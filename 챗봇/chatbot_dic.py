import os, sys, re, json, random, glob, time
import urllib.request
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from gensim.models import Word2Vec
from tqdm import tqdm

okt = Okt()
w2v = Word2Vec.load('dialogue/w2v.model')

dic = {}
root_dir = 'dialogue'
dic_file = 'dialogue/markov-kakao.json' # 없으면 생성

#######################################################
# 텍스트 파일을 받아 형태소 분석하여 리스트로 반환
#######################################################

def make_morph(text):
    '''
    텍스트 파일을 받아 형태소 분석하여 리스트로 반환
    (구두점 제외)
    '''
    # start = time.time()
    morph_list = okt.pos(text, norm=True)
    # print(morph_list[:100])

    word_list = []
    for morph in morph_list:
        # 마침표를 제외한 모든 구두점 제외
        if not morph[1] in ['Punctuation']:
            word_list.append(morph[0])
        if morph[0] == '.':
            word_list.append(morph[0])
    # print(word_list)
    # sys.exit(0)
    # print(f'형태소 분석 작업 완료.\n형태소 분석 작업에 {(time.time - start)/60}분이 소요되었습니다.')

    return word_list


###########################################################
# 형태소 분석 자료 이용해 사전 파일 만들어 반환 
###########################################################

def make_dic(word_list):
    '''
    형태소 분석 자료 이용해 사전 파일 만들어 반환(딕셔너리 자료형) 
    '''
    global dic
    if len(word_list) == 0: return
    tmp = ['@']
    for i, word in enumerate(word_list):
        if word == '' or word =='\r\n' or word == '\n': continue

        tmp.append(word)
        if len(tmp) < 3: continue      # 3개 단어씩 묶기
        if len(tmp) > 3: tmp = tmp[1:] # tmp 리스트 길이가 3을 넘어가면 첫 번째 요소 제외
        # print(tmp)
        # sys.exit(0)

        w1, w2, w3 = tmp 
        if not w1 in dic: dic[w1] = {}   # w1 단어가 사전에 없으면 등록
        if not w2 in dic[w1]: dic[w1][w2] = {}  # w2 단어가 w1 블록 안에 없으면 등록
        if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0 # w3 단어가 w2 블록 안에 없으면 등록 후 0으로 초기화
        dic[w1][w2][w3] += 1   # w3 단어가 나왔기 때문에 +1
        
        if word == '.' or word == '?':  # 마침표를 만나면 tmp 초기화
            tmp = ['@']
            continue

    # print('사전:\n', dic)  # @로 시작해서 .로 끝나는 딕셔너리
    # sys.exit(0)
    
    # 사전 파일이 변경될 때마다 저장하기
    json.dump(dic, open(dic_file, 'w', encoding='utf-8'))


###############################################
# 사전 파일 이용해 문장 생성 
###############################################

def word_choice(sel):
    '''
    사전 파일의 키 목록을 받아 무작위로 하나 선택해 반환
    '''
    keys = sel.keys()
    #print(keys)
    return random.choice(list(keys))

def make_sentence(head):
    '''
    사전 파일 이용해 문장 생성
    '''
    if not head in dic: return '' #입력 단어가 없으면 빈 문자 반환. but, 입력 단어 없으면 @를 받기 때문에 이 코드는 실행 안 될 듯

    ret = []
    if head != '@': ret.append(head)  # @가 아니면 입력 단어를 리스트에 추가
    top = dic[head]
    w1 = word_choice(top) # 입력 단어 하위에 있는 단어 무작위로 선택
    w2 = word_choice(top[w1])  # 그 단어 하위에 있는 단어 무작위로 선택
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:     # w1, w2 값 중 무작위로 선택해 w3에 저장
            w3 = word_choice(dic[w1][w2])
        else: w3 = ''
        ret.append(w3)
        if w3 == '.' or w3 == '?' or w3 == '\n': break  # 마침표, 물음표, 공백을 만나면 멈춤
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

#############################################################################
# STAR : 사전 파일 없으면 만들고 / 있으면 로드 -> 문장 생성
#############################################################################

# 사전 파일이 없다면
# 형태소 분석 -> 사전 파일 생성 -> json 파일로 저장


if os.path.exists(dic_file):
    dic = json.load(open(dic_file, 'r'))
else:

    # ## 폴더 내의 여러 파일 변환
    # i = 0
    # # 문장 읽어 들이기
    # for dirs in os.listdir(root_dir):  # dialogue/ 내의 txt 파일 읽기
    #     dir_path = root_dir + '/' + dirs
    #     if not os.path.isdir(dir_path): continue # 폴더가 아니면 지나가기
    #     sns_files = glob.glob(dir_path+'/*.txt')
    #     for sns_file in sns_files:        
    #         with open(sns_file, 'r') as f:
    #             text = f.read()
    #             # 매 줄 앞의 숫자와 공백 없애기
    #             text = re.sub('^[0-9] : ', '', text, flags=re.MULTILINE)
    #             # 공백을 나타내는 \xa0 유니코드 삭제
    #             text = re.sub('\xa0', ' ', text, flags=re.MULTILINE)
    #             # 줄바꿈 문자 앞에 마침표 추가
    #             text = re.sub('[\?+\!+\.+\n]', '.', text )
    #             text = re.sub('\.+', '.', text )
    #             text = text + '.'
    #             # print(text)
    #             # sys.exit(0)

    #         # 형태소 분석 -> 사전 생성 -> json 파일로 저장
    #         word_list = make_morph(text)
    #         make_dic(word_list)
    #         i += 1
    #         print(f'{i} 개의 파일이 사전으로 만들어졌습니다.')

    # 한 개 폴더 내의 모든 파일 변환
    sns_files = glob.glob('dialogue/kakao1/*.txt')
    for sns_file in tqdm(sns_files[:10001]):  # range 대신에 tqdm을 쓰면 진행 상태바를 나타낸다.
        with open(sns_file, 'r') as f:
            text = f.read()
            # 공백을 나타내는 \xa0 유니코드 삭제
            text = re.sub('\xa0', ' ', text, flags=re.MULTILINE)
            # 줄바꿈 문자 앞에 마침표 추가
            text = re.sub('[\?+\!+\.+\n]', '.', text )
            text = re.sub('\.+', '.', text )
            text = text + '.'
            # 형태소 분석 -> 사전 생성 -> json 파일로 저장
            word_list = make_morph(text)
            make_dic(word_list)

print('ok')

with open(dic_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
# print(json.dumps(json_data, ensure_ascii=False, indent=4))

#############################################################################
# 챗봇 응답 만들기
#############################################################################

def make_reply(text):
    '''
    사용자가 입력한 텍스트를 사전에 등록 후 json 파일에 저장
    사전에 사용자가 입력한 텍스트가 없으면 사전 전체에서 무작위로 문장 생성
    사전에 사용자가 입력한 텍스트가 있으면 그것을 기반으로 문장 생성
    '''
    # 단어 학습시키기
    if not text[-1] in ['.', '?']: text += '.' # 점으로 문장 구분. 마침표나 물음표 없으면 마침표 추가
    word_list = make_morph(text) 
    make_dic(word_list)

    # 사용자가 입력한 텍스트에서 명사만 추출 후 하나를 랜덤하게 골라
    # word2vec 학습한 모델에서 가장 유사한 단어 추출한 후 
    # 그것을 기반으로 문장 만들기
    try:
        face = random.choice(word_list)
        face = w2v.wv.most_similar(face)[0][0]
        if face in dic: return make_sentence(face)
    except: pass

    return make_sentence('@')
