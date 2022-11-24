import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Okt 
okt = Okt()
malist = okt.pos('아버지가방에들어가신다.', norm=True, stem=True)
print(malist)

# 토지 텍스트 파일 열기
fp = codecs.open('../data/BEXX0003.txt', 'r', encoding='utf-16')
soup = BeautifulSoup(fp, 'html.parser')
body = soup.select_one('body > text')
text = body.getText()

# 텍스트 한 줄씩 처리하기
word_dic = {}
lines = text.split('\n') # 줄 구분 문자 단위로 나누기
for line in lines:
    malist = okt.pos(line)
    for word in malist:
        if word[1] == 'Noun':    # 명사이면
            if not (word[0] in word_dic):  # 사전에 명사가 없으면 추가하고 0으로 초기화
                word_dic[word[0]] = 0
            word_dic[word[0]] += 1     # 카운트 +1

# 많이 사용된 명사 50개 출력 - (명사, 등장횟수)
keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True) # 카운트 역순으로 정렬
for word, count in keys[:50]:
    print('{0}({1}) '.format(word, count), end='')
print()

