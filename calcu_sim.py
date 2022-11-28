import pandas as pd
import numpy as np
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('book.csv')

# 제 컴퓨터로는 데이터 개수를 줄여야 돌아갑니다...
df1 = df.head(3000)

description = df1['description']

# TF - IDF 기법으로 벡터화
# 20000개의 줄거리는 약 80000개의 단어로 이루어져있다. (전처리 완료돼서 많이 줄었다.)
tf_idf = TfidfVectorizer()
tf_idf_matrix = tf_idf.fit_transform(description)
# print('TF-IDF 행렬의 크기(shape) :',tf_idf_matrix.shape)

# 전체 유사도 계산
cos_sim = cosine_similarity(tf_idf_matrix, tf_idf_matrix)
# print('코사인 유사도 연산 결과 :',cos_sim.shape)

# 도서 제목 입력하면 인덱스를 리턴
# idx = title_idx['Whispers of the Wicked Saints']

np.save('./sim.npy', cos_sim)