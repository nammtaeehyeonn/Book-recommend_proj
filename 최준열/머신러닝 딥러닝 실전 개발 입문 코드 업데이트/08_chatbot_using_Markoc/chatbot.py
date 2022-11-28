import codecs
from bs4 import BeautifulSoup
import urllib.request
from konlpy.tag import Okt
import os, re, json, random

dict_file = 'chatbot-data.json'
dic = {}
okt = Okt()

# 사전에 단어 등록
def register_dic(words):
    global dic
    if len(words) == 0: return
    tmp = ['@']
    for i in words:
        word = i[0]
        if word == '' or word == '\r\n' or word == '\n': continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == '.' or word == '?':
            tmp = ['@']
            continue
    # 사전이 변경될 때마다 저장하기
    json.dump(dic, open(dict_file, 'w', encoding='utf-8'))

# 사전에 글 등록
def set_word3(dic, s3):
    w1, w2, w3 = s3   # 3개씩 묶은 단어를 각각의 변수에 할당
    if not w1 in dic: dic[w1] = {}   # w1 단어가 사전에 없으면 등록
    if not w2 in dic[w1]: dic[w1][w2] = {}  # w2 단어가 w1 블록 안에 없으면 등록
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0 # w3 단어가 w2 블록 안에 없으면 등록 후 0으로 초기화
    dic[w1][w2][w3] += 1   # w3 단어가 나왔기 때문에 +1

# 문장 만들기
def make_sentence(head):
    if not head in dic: return ''
    ret = []
    if head != '@': ret.append(head)  # 문장의 시작을 나타내는 @가 아니면 리스트에 추가
    top = dic[head]
    w1 = word_choice(top) # 문장을 무작위로 선택. @가 문장의 시작을 표시
    w2 = word_choice(top[w1])  # 문장 중 첫 번째 단어를 무작위로 선택
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ''
        ret.append(w3)
        if w3 == '.' or w3 == '? ' or w3 == '': break
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

# 챗봇 응답 만들기
def make_reply(text):
    # 단어 학습시키기
    if not text[-1] in ['.', '?']: text += '.'
    words = okt.pos(text, norm=True, stem=True)
    register_dic(words)

    # 사전에 단어가 있으면 그것을 기반으로 문장 만들기
    for word in words:
        face = word[0]
        if face in dic: return make_sentence(face)
    return make_sentence('@')

# 사전이 있으면 읽어들이기
if os.path.exists(dict_file):
    dic = json.load(open(dict_file, 'r'))

########################
os.system('clear')
q = 1
print('대화를 끝내려면 ctrl + c 키를 누르세요\n')
while q != 0:
    user = input('>>> ')
    if user == '': continue
    res = make_reply(user)
    print('{:>200}'.format('<<< 챗봇'))
    print(res.rjust(20))
    print()
    #q = int(input('대화를 끝내려면 0번을 누르세요>>> '))
    
