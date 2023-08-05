import re


from tqdm import tqdm

def remove_special_char(corpus : list) -> list: #특수문자 제거
        return [' '.join(re.sub(r"[^가-힣ㄱ-ㅎa-zA-Z0-9/\+\-()\[\]&~.,'\s]"," ",i).split()) for i in tqdm(corpus)]

def remove_ja(corpus):  #한글 자음 제거
    return [' '.join(re.sub(r"[ㄱ-ㅎ]"," ",i).split()) for i in tqdm(corpus)]

def remove_mo(corpus):  #한글 모음 제거
    return [' '.join(re.sub(r"[ㅏ-ㅣ]"," ",i).split()) for i in tqdm(corpus)]

def dot_char_to_word(corpus): #소수점을 dot으로 치환
    return [re.sub(r'(\d+)\.(\d+)',r"\1dot\2", i) for i in tqdm(corpus)]

def dot_word_to_char(corpus): #dot으로 치환 소수점으로 치환
    return [re.sub('[dot]','.', i) for i in tqdm(corpus)]

def convert_plus(corpus): #+를 plus로 치환
    return [re.sub('[+]','플러스',i) for i in tqdm(corpus)]

def convert_upper_to_lower(corpus): #영문 대문자를 소문자로 치환
    corpus = [i.lower() for i in tqdm(corpus)]
    return corpus
    
# def spacing_type_based(corpus : list)->list: #문자 타입별 띄어쓰기
#     pattern = re.compile('([a-z]+|[0-9]+|[가-힣]+)')
#     corpus = [' '.join(pattern.sub(r' \1', i).split()) for i in tqdm(corpus)]
#     return corpus

def spacing_next_hangeul(corpus : list)->list: #문자 타입별 띄어쓰기
    pattern = re.compile('([가-힣]+)([a-zA-Z1-9]+)')
    corpus = [' '.join(pattern.sub(r'\1 \2', i).split()) for i in tqdm(corpus, position=0)]
    return corpus

def spacing_next_english(corpus : list)->list: #문자 타입별 띄어쓰기
    pattern = re.compile('([a-zA-Z]+)([가-힣]+)')
    corpus = [' '.join(pattern.sub(r'\1 \2', i).split()) for i in tqdm(corpus, position=0)]
    return corpus
    
    