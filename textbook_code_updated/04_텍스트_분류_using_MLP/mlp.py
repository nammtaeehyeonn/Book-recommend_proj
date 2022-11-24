import os, glob, json

root_dir = '../data'
dic_file = root_dir + '/word-dic.json'        # 로드할 파일
data_file = root_dir + '/data.json'           # 생성할 파일
data_file_min = root_dir + '/data-mini.json'  # 생성할 파일

# 어구를 자르고 ID로 변환
word_dic = {"_MAX": 0}
def text_to_ids(text):
    text = text.strip()
    words = text.split(" ")
    result = []
    for n in words:
        n = n.strip()
        if n == "": continue
        if not n in word_dic:
            wid = word_dic[n] = word_dic["_MAX"]
            word_dic["_MAX"] += 1
            print(wid, n)
        else:
            wid = word_dic[n]
        result.append(wid)
    return result

# 파일 읽고 고정 길이의 배열 리턴
def file_to_ids(fname):
    with open(fname, 'r') as f:
        text = f.read()
        return text_to_ids(text)

# 딕셔너리에 단어 모두 등록
def register_dic():
    files = glob.glob(root_dir+ '/*/*.txt', recursive=True)
    for i in files:
        file_to_ids(i)

# 파일 내부의 단어 세기
def count_file_freq(fname):       # txt 파일명을 받아
    cnt = [0 for n in range(word_dic["_MAX"])] # 단어사전의 아이디를 cnt 변수에 담기
    with open(fname, 'r') as f:  # txt 파일을 열어
        text = f.read().strip()
        ids = text_to_ids(text) # 단어장 등록
        for wid in ids:         # 단어장에 있는 단어의 수만큼 cnt 증가
            cnt[wid] += 1
    return cnt

# 카테고리마다 파일 읽기
def count_freq(limit = 0):
    X = []
    Y = []
    max_words = word_dic["_MAX"]
    cat_names = []
    for cat in os.listdir(root_dir):  # data/ 안의 카테고리(100 - 105) 폴더 내의 txt 파일 읽기
        cat_dir = root_dir + '/' + cat
        if not os.path.isdir(cat_dir): continue # 폴더가 아니면 지나가기
        cat_idx = len(cat_names)  # 카테고리 길이를 카테고리 아이디로 사용
        cat_names.append(cat)    # 폴더명을 카테고리 이름으로 사용
        files = glob.glob(cat_dir+'/*.txt')
        i = 0
        for path in files:
            print(path)
            cnt = count_file_freq(path)
            X.append(cnt)        # X는 단어 출현 빈도
            Y.append(cat_idx)    # Y는 카테고리
            if limit > 0:
                if i > limit: break
                i += 1
    return X, Y

# 단어 딕셔너리 만들기
if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    register_dic()
    json.dump(word_dic, open(dic_file, 'w'))

# 벡터를 파일로 출력
# 테스트 목적으로 소규모 데이터 만들기
X, Y = count_freq(20)
json.dump({'X':X, 'Y':Y}, open(data_file_min, 'w'))

# 전체 데이터를 기반으로 데이터 만들기
X, Y = count_freq()
json.dump({'X':X, 'Y':Y}, open(data_file, 'w'))
print('ok')

