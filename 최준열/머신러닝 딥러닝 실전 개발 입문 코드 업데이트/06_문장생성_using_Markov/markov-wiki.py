import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Okt
import urllib.request

import os, re, json, random

# 마르코프 체인 딕셔너리 만들기
def make_dic(words):
    tmp = ['@']
    dic = {}
    for word in words:
        tmp.append(word)
        if len(tmp) < 3: continue      # 3개 단어씩 묶기
        if len(tmp) > 3: tmp = tmp[1:] # tmp 리스트 길이가 3을 넘어가면 첫 번째 요소 제외
        set_word3(dic, tmp) # dic 딕셔너리에 tmp 등록
        if word == '.':  # 마침표를 만나면 tmp 초기화
            tmp = ['@']
            continue
    print('사전', dic)  # @로 시작해서 .로 끝나는 딕셔너리
    return dic

# 딕셔너리에 데이터 등록
def set_word3(dic, s3):
    w1, w2, w3 = s3   # 3개씩 묶은 단어를 각각의 변수에 할당
    if not w1 in dic: dic[w1] = {}   # w1 단어가 사전에 없으면 등록
    if not w2 in dic[w1]: dic[w1][w2] = {}  # w2 단어가 w1 블록 안에 없으면 등록
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0 # w3 단어가 w2 블록 안에 없으면 등록 후 0으로 초기화
    dic[w1][w2][w3] += 1   # w3 단어가 나왔기 때문에 +1

# 문장 만들기
def make_sentence(dic):
    ret = []
    if not '@' in dic: return 'no dic'  # 문장의 시작을 나타내는 @가 없으면 사전이 없다는 문자열 반환
    top = dic['@']
    w1 = word_choice(top) # 문장을 무작위로 선택. @가 문장의 시작을 표시
    w2 = word_choice(top[w1])  # 문장 중 첫 번째 단어를 무작위로 선택
    ret.append(w1)
    ret.append(w2)
    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == '.': break
        w1, w2 = w2, w3
    ret = ''.join(ret)

    # 띄어쓰기
    params = urllib.parse.urlencode({
        '_callback':'',
        'q':ret
        })

    # 네이버 맞춤법 검사기 사용
    request = urllib.request.Request('https://m.search.naver.com/p/csearch/ocontent/spellchecker.nhn?' + params)
    request.add_header('Referer', 'https://search.naver.com/search.naver')
    data = urllib.request.urlopen(request)
    data = data.read().decode('utf-8')[1:-2]
    data = json.loads(data)
    data = data['message']['result']['html']
    data = soup = BeautifulSoup(data, 'html.parser').getText()

    return data

def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

# 문장 읽어 들이기
wiki_file = '../data/kowiki.txt'
dict_file = 'markov-wiki.json'
if not os.path.exists(dict_file):  # dict 파일(markov-wiki.json) 만들기
    # 위키 텍스트 파일 읽기
    fp = codecs.open(wiki_file, 'r', encoding='utf-8')

    # 형태소 분석
    okt = Okt()
    words = []
    while True:
        text = fp.readline()
        if not text: break
        malist = okt.pos(text, norm=True)
        #words = []
        for word in malist:
            # 마침표를 제외한 구두점 제외
            if not word[1] in ['Punctutaion']:  # 단어의 품사가 구두점이면
                words.append(word[0])
            if word[0] == '.':         # 단어가 마침표이면
                words.append(word[0])
       
    # 딕셔너리 생성
    dic = make_dic(words)
    json.dump(dic, open(dict_file, 'w', encoding='utf-8'))
else:
    dic = json.load(open(dict_file, 'r'))

# 문장 만들기
for i in range(3):
    s = make_sentence(dic)
    print(s)
    print('------')


