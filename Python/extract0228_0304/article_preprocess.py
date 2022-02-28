# -*- coding: utf-8 -*-
"""ANLKP전처리모듈.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AyV2-p45AnOUy4EXTwwvXwGRiG2BlHFU
"""

import pandas as pd
import re
from collections import Counter

###### 기사 전처리 함수
def preprocess_article(df):
    """
     기사 데이터 본문 전처리 및 고유명사 리스트 컬럼 추가
     df : 데이터프레임,
     return : 본문전처리 + 고유명사 컬럼 데이터프레임

    """
    # 언론사 리스트 추출
    sources = source_list(df)

    # 고유 명사 추출 -> 고유명사 컬럼에 추가
    df['proper_nouns'] = df['article']
    df['proper_nouns'] = df['proper_nouns'].apply(lambda x: extract_proper_nouns(x))

    # 기사 전처리 함수
    df['article'] = df['article'].apply(lambda x : preprocessing_text(x, sources))
    # print(new_df['article'][2])

    train_preprocessed = df

    # 전처리 파일 저장
    # file_name = str('extract0228_0304/Article_preprocessed/preprocessed_article_' + cate + '_' + str(date1) + '_' + str(date2) + '.csv')
    # save_data(train_preprocessed, file_name)

    return train_preprocessed


# 전처리할 데이터 불러오기 및 결측치 처리
def set_data(df):
    df = df.drop(['url'], axis=1)
    df.dropna(inplace=True)
    return df


# 카테고리 리스트
def category_list(df):
    df_new = df.drop_duplicates(subset="category")
    cate_list = sorted(df_new['category'].astype(str))
    return cate_list


# (전체 기사 전처리 후) 기사 카테고리 별로 분리
def split_data_cate(df, version, path):
    """
    데이터 카테고리별로 분리 및 저장
    df : pandas.Dataframe , version : int
    """
    cate_list = category_list(df)
    for category in cate_list:
        df_cate = df[df['category'] == category]
        save_data(df_cate, path + '/preprocessed_' + category + '_V' + str(version) + '.csv')


# 언론사 리스트 추출
def source_list(df):
    df_new = df.drop_duplicates(subset="source")
    source = sorted(df_new['source'].astype(str))
    return source


# 고유명사 추출
def extract_proper_nouns(docs):
  """
  ''안의 고유명사 리스트 추출(+ 각 문서내 중복 고유명사 제거)

  :param df_article: ※※전처리 전※※ 데이터 프레임 내 기사
  :return: 추출한 고유명사
  """

  proper_nouns = []
  # sum=0
  # for docs in df_article:
  proper_noun = re.findall("'[A-Za-z0-9가-힣 ]+'", str(docs))
  proper_noun = proper_noun + re.findall('‘[A-Za-z0-9가-힣 ]+’', str(docs))

  # sum += len(proper_noun)
  proper_noun = set(proper_noun)
  proper_noun = list(proper_noun)
  proper_nouns = [word.replace(' ', '').replace('‘', '').replace('’', '').replace("'", '') for word in proper_noun]
  # proper_nouns.append(no_space_proper_noun)

  # f_proper_nouns_dict = dict()
  # result = Counter(proper_nouns)
  # for key, value in result.items():
  #   if value >= frequency:
  #     f_proper_nouns_dict[key] = value

  return proper_nouns




def preprocessing_text(docs, source_list):
    """
    정규표현식으로 이메일, 언론사, 기자 이름, 특수문자 제거, 한음절 글자 제거
    연속된 띄어쓰기 -> 단일 띄어씌기로 통일

    :param df: 카테고리, 기간 분할한 데이터 프레임
    :param source_list: 언론사 리스트
    :return: 기사가 전처리된 데이터 프레임
    """
    # new_docs = []
    # for docs in article:

    #이메일 제거
    new_doc = re.sub('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+','',str(docs))
    r_num = new_doc.rfind(',')
    if new_doc[r_num:].rfind('기자'):
        new_doc = new_doc = str(new_doc[0:r_num+1])
    if new_doc[r_num:].rfind('특파원'):
        new_doc = new_doc = str(new_doc[0:r_num+1])
    l_num = new_doc.find(' = ')
    new_doc = str(new_doc[l_num+1:])

    #언론사 제거
    for word in source_list:
        new_doc = re.sub(word,' ', new_doc)

    #특수문자 제거
    new_doc = re.sub('[^A-Za-z0-9가-힣”’-]', ' ', new_doc)
    new_doc = new_doc.replace('”', '')
    new_doc = new_doc.replace('’', '')
    new_doc = new_doc.strip()
    new_doc = ' '.join(new_doc.split())

    #한음절 글자 제거
    new_doc = re.sub(' . ',' ', new_doc)
    new_doc = re.sub(' . ',' ', new_doc)
    new_doc = re.sub(' . ',' ', new_doc)
    # new_docs.append(new_doc)

    # 숫자만 있는 글자 제거
    new_doc = re.sub(' [0-9]+ ', ' ', new_doc)

    # 숫자+글자(공백전까지) 제거
    new_doc = re.sub(' [0-9]+[A-Za-z가-힣]+', ' ', new_doc)
    new_doc = re.sub(' [0-9]+[A-Za-z가-힣]+', ' ', new_doc)
    new_doc = re.sub(' [0-9]+[A-Za-z가-힣]+', ' ', new_doc)

    # df['article'] = pd.DataFrame(new_docs)
    return new_doc

# 전처리 된 데이터 저장

def save_data(df, name):
    df.to_csv(name, encoding='utf-8-sig', index=False)

