# from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
from konlpy.tag import Mecab
import extract0228_0304.word_extract as word_extract
# import extract0228_0304.article_preprocess as preprocess
import re
import os
import time
import datetime




# 전체 기사 전처리 파일 카테고리 별로 분리
# p_df=pd.read_csv("extract0228_0304/Article_preprocessed/전처리완료데이터V5.csv")
# p_df.isna().sum()
# p_df.drop(['Unnamed: 0'], axis=1, inplace=True)
# p_df['proper_nouns'] = p_df['proper_nouns'].fillna('')
# p_df.dropna(inplace=True)
# p_df.groupby(['category']).count()['article']
# preprocess.split_data_cate(p_df,5,"extract0228_0304/Article_preprocessed")


# 플라스크
# app = Flask(__name__)

'''
## 신조어 딕셔너리 생성함수
def get_new_word_information(article_df):
    # url 기사가 해당하는 카테고리 csv 파일 불러오기, 이전 추출된 신조어 불러오기
    path_preprocessed, path_new_words = 'extract0228_0304/Article_preprocessed', 'extract0228_0304/new_words'  # 전처리 파일 저장 경로
    preprocessed_files, new_words_files = os.listdir(path_preprocessed), os.listdir(path_new_words)  # 전체 파일 목록
    cate = article_df['category'][0]
    week = article_df['week'][0]
    for preprocessed_file in preprocessed_files:  # 파일 목록 중에
        if (cate in preprocessed_file) & ("V5" in preprocessed_file):  # 카테고리 및 버전에 따른 파일 이름 선택해서 불러오기
            train_processed = pd.read_csv(str(path_preprocessed + '/' + preprocessed_file), encoding='utf-8-sig')
    for new_words_file in new_words_files:  # 파일 목록 중에
        if (cate in new_words_file) & ("V5" in new_words_file):  # 카테고리 및 버전에 따른 파일 이름 선택해서 불러오기
            new_words_pre = pd.read_csv(str(path_new_words + '/' + new_words_file), encoding='utf-8-sig')

    comp_corpus = list(new_words_pre.new_word)

    # 그 파일 내에서 url 기사가 해당하는 주만 데이터 프레임 저장
    train_data=train_processed.copy()
    train_processed_week = train_data[train_data['week'] == week]

    ## 결측치 처리
    train_processed_week.dropna(inplace=True)

    # 모델링 돌림 - soy 추출, mecab 추출, 고유명사, stop_pos 해당하는 단어
    # 이 단계 별로 딕셔너리에 저장
    stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC', 'EF', 'VV', 'SY SN', 'JX', 'MAG', 'JKB']

    model_dict = word_extract.flask_extract_nouns_list_week(train_processed_week, article_df, cate, week,
                                                            stop_pos=stop_pos, comp_corpus=comp_corpus)

    return model_dict



@app.route("/") # 메인 페이지
def index():
    return render_template("index.html")
        # templates 폴더에 index.html 작성


@app.route("/preprocess_article", methods = ["POST"]) # 기사 전처리 라우트 함수
def preprocess_article():
    # 데이터 불러오기
    df = pd.read_csv('Article/최종기사데이터.csv')
    # url = request.form.get("url")
    # 예제 URL
    url = 'https://news.v.daum.net/v/EOleJemQOS'
    # 언론사 목록 리스트로 저장
    df_new = df.drop_duplicates(subset="source")
    source = sorted(df_new['source'].astype(str))
    l_source = []
    for word in source:
        new_word = re.sub('[^A-Za-z0-9가-힣”’]', '', word)
        if new_word != '':
            l_source.append(new_word)
    l_source = list(set(l_source))

    # 딕셔너리 index
    idx = 1
    # 딕셔너리
    text = {}
    # 해당 url인 기사 정보 데이터프레임으로 저장장
    df = df[df['url'] == url]
    # 인덱스 초기화
    df.reset_index(drop=True, inplace=True)

    # 전처리 시작
    for article in df['article']:
        highlight_words = []
        word_list = []
        # 1. 기사본문 보여주기
        text[str(idx)] = str(article)
        idx += 1
        # 2. 영어본문제거
        if len(re.findall('[가-힣]', str(article))) == 0:
            article = None
        elif (len(re.findall('[가-힣]', str(article))) / len(str(article)) * 100) <= 10:
            article = None
        else:
            article = str(article)

        text[str(idx)] = article
        idx += 1
        # 3. 이메일 제거
        word_list = list(set(re.findall('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', article)))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 4. 기자 이름 제거V1
        word_list = list(set(re.findall('[가-힣 ]+ ?기자', article) + re.findall('[가-힣 ]+ ?특파원', article)))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 5. 기자 이름 제거V2
        word_list = list(set(re.split(r'[^A-Za-z0-9가-힣]', str(df['name'][0]))))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 6. (지역=언론사) 양식
        word_list = list(set(re.findall('[A-Za-z가-힣 ]+=[가-힣0-9 ]+', article)))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 7. 홑 따옴표 안에 문자열 제거
        word_list = list(set(re.findall('‘.+?’', article)))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 8. 특수문자 제거(띄어쓰기)
        article = re.sub('[^A-Za-z0-9가-힣-]', ' ', article)
        article = article.strip()
        article = ' '.join(article.split())

        text[str(idx)] = article
        idx += 1

        # 9. 언론사 제거
        cnt = 0
        for word in l_source:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in l_source:
            article = re.sub(word, '', article)

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 10. 한음절 글자 제거
        for i in range(5):
            cnt = 0
            word_list = list(set(re.findall(' . ', article)))
            if len(word_list) > 0:
                for word in word_list:
                    highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
                    if cnt == 0:
                        highlighted = re.sub(word, highlight_words, article)
                    else:
                        highlighted = re.sub(word, highlight_words, highlighted)
                    cnt += 1
                for word in word_list:
                    article = re.sub(word, ' ', article)
                    article = article.strip()
                    article = ' '.join(article.split())
                text[str(idx)] = highlighted
                idx += 1
            else:
                break
        word_list = []
        highlight_words = []
        cnt = 0

        # 11. 숫자만 있는 글자 제거
        word_list = list(set(re.findall(' [-]?[0-9]+ ', article)))
        cnt = 0
        for word in word_list:
            highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
            if cnt == 0:
                highlighted = re.sub(word, highlight_words, article)
            else:
                highlighted = re.sub(word, highlight_words, highlighted)
            cnt += 1
        for word in word_list:
            article = re.sub(word, '', article)
            article = article.strip()
            article = ' '.join(article.split())

        text[str(idx)] = highlighted
        idx += 1
        word_list = []
        highlight_words = []
        cnt = 0

        # 12. 숫자+글자(공백전까지) 제거(+,-)
        for i in range(5):
            cnt = 0
            word_list = list(set(re.findall(' [-]?[0-9]+[A-Za-z가-힣]+', article)))
            if len(word_list) > 0:
                for word in word_list:
                    highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
                    if cnt == 0:
                        highlighted = re.sub(word, highlight_words, article)
                    else:
                        highlighted = re.sub(word, highlight_words, highlighted)
                    cnt += 1
                for word in word_list:
                    article = re.sub(word, ' ', article)
                    article = article.strip()
                    article = ' '.join(article.split())
                text[str(idx)] = highlighted
                idx += 1
            else:
                break
        word_list = []
        highlight_words = []
        cnt = 0

        # 13. (-)+글자 제거
        for i in range(5):
            cnt = 0
            word_list = list(set(re.findall(' [-][A-Za-z가-힣]+ ', article)))
            if len(word_list) > 0:
                for word in word_list:
                    highlight_words = word.replace(word, '<font class="delete-word">' + word + '</font>')
                    if cnt == 0:
                        highlighted = re.sub(word, highlight_words, article)
                    else:
                        highlighted = re.sub(word, highlight_words, highlighted)
                    cnt += 1
                for word in word_list:
                    article = re.sub(word, ' ', article)
                    article = article.strip()
                    article = ' '.join(article.split())
                text[str(idx)] = highlighted
                idx += 1
            else:
                break
        word_list = []
        highlight_words = []
        cnt = 0

        # 14. 전처리 완료
        text[str(idx)] = article

    answer = text
    response = make_response(jsonify(answer))
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route("/get_new_words", methods=["POST"]) # 신조어 추출 라우트 함수
def get_new_words():
    articles = pd.read_csv("Article/최종기사데이터.csv", encoding='utf-8')
    article_one = articles[articles['url'] == 'https://news.v.daum.net/v/EOleJemQOS'].reset_index(drop=True)
    new_word_information = get_new_word_information(article_one)
    print(new_word_information)

    response = make_response(jsonify(new_word_information))
    response.headers.add("Access-Control-Allow-Origin","*")

    return response

'''

p_df = pd.read_csv("extract0228_0304/Article_preprocessed/preprocessed_사회_V5.csv")
df = p_df.copy()
df['proper_nouns']=df['proper_nouns'].fillna('')
df_society_week1 = df[df['week'] =='1주차' ]

# 비교사전 로드
mecab_new_corpus = pd.read_csv("mecab_new_corpus.csv",encoding="cp949")
new_word_list_pre= list(mecab_new_corpus.단어.unique())
nia_dic = pd.read_csv('NIADic.csv', encoding='cp949')
nia_term_list= list(nia_dic.term.unique())
comp_corpus = list(set(new_word_list_pre + nia_term_list))

# 명사 제외할 pos 태깅
stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC','EF','VV', 'SY SN', 'JX', 'MAG','JKB'] # XSA- ~한, ETM- ~한,
# JKB: ~으로
# SY SN : 음수 제거
# MAG : 게다가, 가득
# JX : 까지
df_new_words = word_extract.extract_nouns_list_week(df_society_week1,
                                            '사회', '1주차',stop_pos=stop_pos, comp_corpus=comp_corpus)

df_new_words.to_csv('new_words_사회_1주차_V6_2.csv',encoding='utf-8-sig', index=False)

if __name__ == '__main__':

    #### flask 서버 연결
    # app.debug = True
    # app.run()

    #### CSV 파일작업
    ### 전처리 파일 저장
    start1 = time.time()
    cate_list = ['IT', '경제', '국제', '문화', '보도자료', '사설칼럼', '사회', '스포츠', '연예', '정치']
    # cate_list = preprocess.create_preprocessed_data("Article/", 4, path = "extract0228_0304/Article_preprocessed")
    end1 = time.time()


    ### 신조어 추출
    start2 = time.time()
    ## 카테고리 여러개 지정해서 여러개 신조어 파일 얻을때
    for cate in cate_list:
        # file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V1_2_proper.csv')
        word_extract.noun_extract_func(cate, "5")

    ## 카테고리 하나 정해서 신조어 파일 하나 얻을때
    # file_name = str('extract0228_0304/new_words/new_words_temp_0301_경제.csv')
    # noun_extract_func("경제", "1_1", file_name=file_name)
    end2 = time.time()

    sec = [end1 - start1, end2 - start2]
    times = [str(datetime.timedelta(seconds=s)).split(".") for s in sec ]
    times = [t[0] for t in times]
    print(times) # 실행 시간 출력

'''
import pandas as pd
import itertools
from collections import Counter
a=pd.read_csv('extract0228_0304/Article_preprocessed/preprocessed_경제_V1_1.csv', encoding='utf-8')
a['prop'] = a['proper_nouns']
a['prop'] = a['prop'].apply(lambda x : x.replace("[","").replace("]","").replace("'","").replace(",",""))

tt=a['prop']
tt = [t.split(' ')for t in tt if t != '']

proper_nouns_all = list(itertools.chain(*tt))

proper_nouns_freq = Counter(proper_nouns_all)
proper_nouns_dict = { proper : freq for proper, freq in proper_nouns_freq.items() if freq >= 10 }
print("=> 고유명사 수 :", len(proper_nouns_dict))

'''



'''
from konlpy.tag import Mecab
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
a={'감사하다':1, '구체적':50, '14일경과':16}

pos = {i: mecab.pos(noun) for i, noun in enumerate(list(a.keys()))}
pos = {noun: mecab.pos(noun) for noun in list(a.keys())}
pos
# 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
# flag = 1 이면 숫자나 단위 있는 단어를 의미
{word : p for word, p in pos.items() if ('씨', 'NNB') in p}
posdict = {}
for noun, pos_list in pos.items():
    pos_str = ""
    for p in pos_list:
        pos_str += ' ' + p[1]
    posdict[noun] = pos_str
posdict

isnum = dict()
stoppos = ['SN', 'NNBC','XSN']
for i, posstr in posdict.items():
    flag = 0
    for pos in stoppos:
        if posstr.find(pos) != -1:
            flag = 1
    isnum[i] = flag

print('=> 숫자 및 단위 포함 명사 수:', sum(isnum.values()))  # 숫자 및 단위 포함된 단어 : 550

# 숫자가 아닌 인덱스만 추출
# ind = [i for i, flag in isnum.items() if flag == 0]

# 숫자 없는 데이터로 추가
a_result = {noun: a[noun] for noun, flag in isnum.items() if flag == 0}  # 숫자 단위 제외 단어 : 5742
print(a_result)
# print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))

'''

