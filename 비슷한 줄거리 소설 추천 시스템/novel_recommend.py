import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# 데이터 파일과 유사도 파일 불러오기
df = pd.read_csv("project_2.csv")
df = df[:5000]
cosine_similarities = np.load('novel_cosine.npy')

def recommendations(title):
    books = df[['Title', 'image']]

    # 책의 제목을 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장.
    indices = pd.Series(df.index, index = df['Title']).drop_duplicates()    
    idx = indices[title]

    # 입력된 책과 줄거리(document embedding)가 유사한 책 5개 선정.
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]

    # 가장 유사한 책 5권의 인덱스
    book_indices = [i[0] for i in sim_scores]

    # 전체 데이터프레임에서 해당 인덱스의 행만 추출. 5개의 행을 가진다.
    recommend = books.iloc[book_indices].reset_index(drop=True)

    fig = plt.figure(figsize=(20, 30))

    # 데이터프레임으로부터 순차적으로 이미지를 출력
    for index, row in recommend.iterrows():
        response = requests.get(row['image'])
        img = Image.open(BytesIO(response.content))
        fig.add_subplot(1, 5, index + 1)
        plt.imshow(img)
        plt.title(row['Title'])
        plt.show()

while True:
    user_input = input('\n끝내려면 q를 입력하세요\n검색할 책 제목을 입력하세요 >>>  ')
    if user_input == 'q':
        break
    
    # 책 제목의 일부 단어만 입력하면 Title 전체 문자열 반환
    try:
        title = df.loc[df['Title'].str.contains(user_input), 'Title']
        title = str(title.values)[2:-2]
    except Exception as e:
        print(f'에러 발생 >>> {e}')

    if title:
        recommendations(title)
    else:
        print('목록에 있는 책 제목을 입력하세요.')

