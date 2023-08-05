import copy
import gc
import itertools
import os

import boto3
import json
import numpy as np
import pickle
import tensorflow as tf

from tqdm import tqdm
from sklearn.metrics import classification_report
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

try:
    from . src.models import bilstm
except:
    from src.models import bilstm


def create_all_hangul_char():
    """ 모든 한글 음절 생성
    """
    hangul = list()
    for i in range(0xAC00, 0xD7A3):
        hangul.append(chr(i))
       
    return hangul

def space_tagging(corpus_list):
    """ character 단위 도큰화와 띄어쓰기 태깅 수행 
    
    """
    words_list = list()
    tags_list = list()
    for corpus in tqdm(corpus_list) :
        sentence = corpus.split(" ")
        tags = list()
        words = list()
        for word in sentence :
            for i,w in enumerate(word) :
                words.append(w)
                if i == 0:
                    tags.append('B')
                else :
                    tags.append('I')
        words_list.append(words)
        tags_list.append(tags)
  
    return (words_list, tags_list)

def sequences_to_tag(sequences, index_to_tag):
    """ 정수화된 태깅을 단어 태깅으로 변경
    """
    result = []
    for sequence in sequences :
        word_list = []
        for index in sequence :
            word_list.append(index_to_tag[index].replace("PAD", "O"))
        
        result.append(word_list)
    return result
    
def postprocessing(X_test, y_predicted):
    """ 예측 데이터 후처리
    """
    final_predicted = list()
    for pred,x in zip(y_predicted,X_test) :
        pred_int = np.argmax(pred, axis = -1)   
        result = list()
        for i,j in zip(pred_int, x):
            if j == 0 :
                result.append(0)
            else :
                result.append(i)
        final_predicted.append(result)
    
    return final_predicted
    
def preprocessing(sentences, tags=False, sent_tokenizer=False, tag_tokenizer=False, max_len=100, tag_size=False):
    """ 입력 데이터와 출력 데이터 전처리
    """
    
    
    X_data = sent_tokenizer.texts_to_sequences(sentences)
    X_data = pad_sequences(X_data, padding='post', truncating='post', maxlen=max_len)

    print('샘플 문장의 크기 : {}'.format(X_data.shape))
    if tags != False : 
        y_data_int = tag_tokenizer.texts_to_sequences(tags)
        y_data_int = pad_sequences(y_data_int, padding='post', truncating='post', maxlen=max_len)
        
        if tag_size == False :
            tag_size = len(set(list(itertools.chain(*y_data_int))))
        
        y_data = to_categorical(y_data_int, num_classes=tag_size)
    
        print('샘플 레이블(정수 인코딩)의 크기 : {}'.format(y_data_int.shape))
        print('샘플 레이블(원-핫 인코딩)의 크기 : {}'.format(y_data.shape))
    
        return X_data, y_data
    
    return X_data
    
def createDirectory(directory): 
    """ 모델 저장 디렉토리 생성
    """
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")

def convert_sentence(X_test, pred_tags, index_to_word):
    """ 예측 결과에 따라 띄어쓰기 교정
    """
    X_test_str = list()
    for sentence in X_test :
        X_test_str.append([index_to_word[i] for i in sentence])
        
        
    result_app_words_list = copy.deepcopy(X_test_str)
    for i, pred_tag in enumerate(pred_tags):
        k = 0
        for j in range(len(pred_tag)):
            if j>0 and pred_tag[j] == 'B':
                result_app_words_list[i].insert(k,' ')
                k+=1
            k+=1
    
    result = list()
    remove_set = {'PAD'}
    for result_app_words in result_app_words_list :
        result.append([i for i in result_app_words if i not in remove_set])
    
    result = [''.join(i) for i in result]
    
    return result

class Corrector(object) :
    """ 띄어쓰기 교정기
    """
    def __init__(self) :
        self.model = None
        self.model_dir = None
        self.sent_tokenizer = None
        self.tag_tokenizer = None
        
        self.s3_bucket_name = "joongna-search"
        self.s3_models_storage_prefix = "ml_models/jn_space_corrector_models"
        
        self.local_models_storage_prefix = 'jn_space_corrector_models'
        
 
    
    def train_tokenizer(self, sentences, tags):
        """ 토크나이저 학습
        """
        
        self.sent_tokenizer = Tokenizer(oov_token='OOV', lower=False)
        self.tag_tokenizer = Tokenizer(lower=False)
        
        self.sent_tokenizer.fit_on_texts(sentences)
        self.tag_tokenizer.fit_on_texts(tags)
        
        self.sent_tokenizer.fit_on_texts(create_all_hangul_char()) #모든 한글 단어 토큰 추가
        
        
        return self.sent_tokenizer, self.tag_tokenizer
        
    
    def config_tokenizer(self, sent_tokenizer, tag_tokenizer) :
        """ 토크나이저 config 설정
        """
        self.vocab_size = len(sent_tokenizer.word_index) + 1
        self.tag_size = len(tag_tokenizer.word_index) + 1
        
        print('단어 집합의 크기 : {}'.format(self.vocab_size))
        print('개체명 태깅 정보 집합의 크기 : {}'.format(self.tag_size))
        
        self.word_to_index = self.sent_tokenizer.word_index
        self.index_to_word = self.sent_tokenizer.index_word
        self.tag_to_index = self.tag_tokenizer.word_index
        self.index_to_tag = self.tag_tokenizer.index_word
        self.index_to_tag[0] = 'PAD'
        self.index_to_word[0] = 'PAD'
        
    
    def training(self, data, file_dir, embedding_dim=128, hidden_units=256, max_len=70, batch_size=128, learning_rate=0.001, epochs=6, validation_split=0.1):
        """ 모델 학습 
        """
        self.embedding_dim = embedding_dim
        self.hidden_units = hidden_units
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split
        
        self.max_len = max_len
        self.train_sentences, self.train_tags = space_tagging(data)
        
        if self.sent_tokenizer == None and self.tag_tokenizer == None :
            self.train_tokenizer(self.train_sentences, self.train_tags)
            
        self.save_tokenizer(file_dir)
        self.config_tokenizer(self.sent_tokenizer, self.tag_tokenizer)
        
        self.X_train, self.y_train = preprocessing(sentences = self.train_sentences, 
                                                                     tags = self.train_tags, 
                                                                     sent_tokenizer = self.sent_tokenizer,
                                                                     tag_tokenizer = self.tag_tokenizer,
                                                                    max_len = self.max_len,
                                                                    tag_size = self.tag_size)
        
        del self.train_sentences, self.train_tags
        
        checkpoint_path = file_dir+"/cp-{epoch:04d}.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        self.save_model_config(checkpoint_dir)
        
        self.model = bilstm(self.vocab_size, self.embedding_dim, self.hidden_units, self.tag_size)
        self.model.save_weights(checkpoint_path.format(epoch=0))
        
        es = EarlyStopping(monitor='val_loss', 
                           mode='min', 
                           verbose=1, 
                           patience=3
                          )
        
        mc = ModelCheckpoint(filepath = checkpoint_path, 
                             #monitor='val_decode_sequence_accuracy', 
                             monitor = 'val_accuracy',
                             mode='max', 
                             verbose=1, 
                             save_best_only=True, 
                             save_freq="epoch",
                             save_weights_only=True
                            )
        
        self.model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate), metrics=['accuracy'])
        self.model.fit(self.X_train, self.y_train, 
                                 batch_size=batch_size, 
                                 epochs=epochs, 
                                 validation_split=validation_split, 
                                 callbacks=[mc, es]
                                )
    
        #self.save_model(checkpoint_path)
    
    def further_training(self, data, new_dir, batch_size=128, epochs=6, learning_rate=0.001, validation_split=0.1):
        """ 모델 추가 학습
        """
        
        self.save_tokenizer(new_dir)

        train_sentences, train_tags = space_tagging(data)
        
        self.X_train, self.y_train = preprocessing(sentences = train_sentences, 
                                                                     tags = train_tags, 
                                                                     sent_tokenizer = self.sent_tokenizer,
                                                                     tag_tokenizer = self.tag_tokenizer,
                                                                     max_len = self.max_len,
                                                                    tag_size = self.tag_size)
        
        del train_sentences, train_tags, data
        
        #checkpoint_path = new_dir+"/"+str(count)+"_cp-{epoch:04d}.ckpt"
        checkpoint_path = new_dir+"/cp-{epoch:04d}.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        
        self.save_model_config(checkpoint_dir)
        
        self.model.save_weights(checkpoint_path.format(epoch=0))

        es = EarlyStopping(monitor='val_loss', 
                           mode='min', 
                           verbose=1, 
                           patience=2
                          )
        
        mc = ModelCheckpoint(filepath = checkpoint_path, 
                             #monitor='val_decode_sequence_accuracy', 
                             monitor = 'val_accuracy',
                             mode='max', 
                             verbose=1, 
                             save_best_only=True, 
                             save_freq="epoch",
                             save_weights_only=True
                            )
        
        self.model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate), metrics=['accuracy'])

        history = self.model.fit(self.X_train, self.y_train, 
                                 batch_size=batch_size, 
                                 epochs=epochs, 
                                 validation_split=validation_split, 
                                 callbacks=[mc, es]
                                )
        return history
        #self.save_model(checkpoint_path)
      
            
    def save_model_config(self, checkpoint_dir):
        """ 모델 config 저장
        """
        model_config={
            'max_len' : self.max_len,
            'embedding_dim' : self.embedding_dim, 
            'hidden_units' : self.hidden_units, 
            'vocab_size' : self.vocab_size, 
            'tag_size' : self.tag_size
        }
        
        path = "{}/model_config.json".format(checkpoint_dir)
        with open(path, "w") as f: 
            json.dump(model_config, f)
        
#     def save_model(self, checkpoint_path):
#         """ 모델 저장 
#         """
#         checkpoint_dir = os.path.dirname(checkpoint_path)
#         self.model.save_weights(checkpoint_path)
#         model_config={
#             'max_len' : self.max_len,
#             'embedding_dim' : self.embedding_dim, 
#             'hidden_units' : self.hidden_units, 
#             'vocab_size' : self.vocab_size, 
#             'tag_size' : self.tag_size
#         }
        
#         path = "{}/model_config.json".format(checkpoint_dir)
#         with open(path, "w") as f: 
#             json.dump(model_config, f)

        
    def save_tokenizer(self, file_dir):
        """ 토크나이저 저장
        """
        
        createDirectory(file_dir)
        
        with open('{}/sent_tokenizer.pickle'.format(file_dir), 'wb') as handle:
            pickle.dump(self.sent_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('{}/tag_tokenizer.pickle'.format(file_dir), 'wb') as handle:
            pickle.dump(self.tag_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
  
    def load_tokenizer(self, file_dir) : 
        with open('{}/sent_tokenizer.pickle'.format(file_dir), 'rb') as handle:
            self.sent_tokenizer = pickle.load(handle)

        with open('{}/tag_tokenizer.pickle'.format(file_dir), 'rb') as handle:
            self.tag_tokenizer = pickle.load(handle)
        
        return self.sent_tokenizer, self.tag_tokenizer
            
            
    def test(self, data, model_dir = False):
        """ 모델 테스트/검증
        """
        
        
        test_sentences, test_tags = space_tagging(data)
        if model_dir != False :
            self.load_pre_trained(model_dir)
            
        
        self.X_test, self.y_test = preprocessing(sentences = test_sentences, 
                                                                     tags = test_tags, 
                                                                     sent_tokenizer = self.sent_tokenizer, 
                                                                     tag_tokenizer = self.tag_tokenizer, 
                                                                     max_len=self.max_len,
                                                                 tag_size = self.tag_size)
        y_predicted = self.model.predict([self.X_test]) # 
        self.y_predicted = postprocessing(self.X_test, y_predicted)
        self.y_test_int = postprocessing(self.X_test, self.y_test)
        
        self.pred_tags = sequences_to_tag(self.y_predicted, self.index_to_tag)
        self.test_tags = sequences_to_tag(self.y_test_int, self.index_to_tag)
        
        self.test_result = classification_report(list(itertools.chain(*self.pred_tags)), list(itertools.chain(*self.test_tags)))
        return self.test_result

    
    
    def correct(self, data, model_dir = False, keep_existing_space = True):
        """ 문장 띄어쓰기 수정
        """
        
        
        test_sentences, self.test_tags = space_tagging(data)
        if model_dir != False :
            self.load_pre_trained(model_dir)
        
        self.X_test = preprocessing(sentences = test_sentences, 
                                          tags = False, 
                                          sent_tokenizer = self.sent_tokenizer, 
                                          tag_tokenizer = False, 
                                          max_len = self.max_len, 
                                   tag_size = self.tag_size)
        
        self.y_predicted = self.model.predict([self.X_test]) # 모델 예측 
        self.y_predicted = postprocessing(self.X_test, self.y_predicted) #예측 값 후처리
        
        self.pred_tags = sequences_to_tag(self.y_predicted, self.index_to_tag) # 숫자 태그를 word 태그로 변경
        
        
        if keep_existing_space == True :
            self.pred_tags = keep_input_spacing_tokens(self.test_tags, self.pred_tags, self.max_len) #입력 데이터의 띄어쓰기 토큰 유지
        
        corrected_data = convert_sentence(self.X_test, self.pred_tags, self.index_to_word) # 예측된 띄어쓰기 태그에 맞게 문장 교정
        #print(result)
        return corrected_data

        
    def load_pre_trained(self, model):
        
        try :
            s3 = boto3.client('s3')
            s3_model_folder = self.s3_models_storage_prefix + '/' + model
            contents_list = s3.list_objects(Bucket = self.s3_bucket_name, Prefix=s3_model_folder)['Contents']
            print("공유 저장소 모델 판별")
            
            try:
                file_list = os.listdir(self.local_models_storage_prefix)
                if model not in file_list :
                    print(file_list)
                    raise Exception('로컬 저장소에 없음')

                
            except Exception as e :
                print(e)
                print('모델 다운로드 : {}'.format(model))
                self.model_download(model_name=model, download_prefix=False)
            
            model = self.local_models_storage_prefix + '/' + model
            self.model_load(model)


        except Exception as e :
            print(e)
            print("개인 저장소 모델 판별")
            self.model_load(model)
        
       
    def model_load(self, model_dir):
        """ 학습된 모델 로드
        """
        
#         if os.path.isdir('.models/'+ model_dir) == True :
#             model_dir = '.models/'+ model_dir
#         print('절대경로:',os.path.abspath(model_dir) )
        self.model_dir = model_dir
        self.sent_tokenizer, self.tag_tokenizer = self.load_tokenizer(self.model_dir) # 토크나이저 로드
        self.config_tokenizer(self.sent_tokenizer, self.tag_tokenizer) #토크나이즈 설정

        
        path = "{}/model_config.json".format(self.model_dir) # 모델 config 로드
        with open(path, "r") as f:
            model_config = json.load(f)
            
        self.max_len = model_config['max_len']
        self.embedding_dim = model_config['embedding_dim']
        self.hidden_units = model_config['hidden_units']
        self.vocab_size = model_config['vocab_size']
        self.tag_size = model_config['tag_size']
        
        
        self.model = bilstm(self.vocab_size, self.embedding_dim, self.hidden_units, self.tag_size) #모델 로드
        latest = tf.train.latest_checkpoint(model_dir)
        self.model.load_weights(latest)
        
        
        
        
        print(model_config)
        
        
        return model_config, self.model, self.sent_tokenizer, self.tag_tokenizer
    
    def model_upload(self, model_dir=False):
        
        
        
        
        if model_dir == False and self.model_dir == None :
            return '현재 지정된 모델이 없습니다.'
        if model_dir != False :
            self.model_dir = model_dir
        
        
        s3 = boto3.client('s3')
        file_list = os.listdir(self.model_dir)
        
        try :
            for name in file_list :
                file_path = self.model_dir + '/' + name
                save_path = self.s3_models_storage_prefix +'/'+ self.model_dir.split('/')[-1]+'/'+name
                print(file_path)
                if os.path.isfile(file_path) : #directory 업로드 항목에서 제외
                    s3.upload_file(file_path, self.s3_bucket_name, save_path)
            return '모델 업로드 완료 : {}'.format(self.model_dir)
        except Exception as e:
            return '모델 업로드 실패 : {}'.format(e)
    
    
    def model_download(self, model_name=False, download_prefix=False):
        if model_name != False :
            self.model_name = model_name
        
        s3 = boto3.client('s3')
        print(self.local_models_storage_prefix + '/' + self.model_name)
        
        if download_prefix == False :
            download_path = self.local_models_storage_prefix + '/' + self.model_name
        else :
            download_path = download_prefix + '/' + self.model_name
            
        createDirectory(download_path)
        
        s3_model_path = self.s3_models_storage_prefix+'/'+model_name

        contents_list = s3.list_objects(Bucket = self.s3_bucket_name, Prefix=s3_model_path)['Contents']
        print("모델 다운로드 ...")
        for contents in tqdm(contents_list) :
            print(contents['Key'])
            file_name = contents['Key'].split('/')[-1]
            s3.download_file(self.s3_bucket_name, contents['Key'], download_path + '/'+file_name)

                    

def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")        
    
def keep_input_spacing_tokens(input_tags, pred_tags, max_len):
    """ 기존 띄어쓰기 유지
    """
    for i in range(len(input_tags)):
        for j in range(len(input_tags[i])):
            if j<max_len and input_tags[i][j]=='B' and pred_tags[i][j]=='I' :
                pred_tags[i][j] = 'B'
            
    return pred_tags