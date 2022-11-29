import streamlit as st
import numpy as np
import pandas as pd
import random

def Recommend(title, cos_sim):
    
    title_idx = dict(zip(df['Title'], df.index))
    # 도서 제목 입력하면 인덱스를 리턴
    idx = title_idx[title]

    # 도서 줄거리 유사도 전부 가져오기
    sim = list(enumerate(cos_sim[idx]))

    # 유사도에 따라 정렬하기
    sim = sorted(sim, key=lambda x: x[1], reverse=True)

    # 유사도 탐5 가져오기
    sim = sim[1:6]

    # 유사도 탑5 인덱스 가져오기
    rec_idx = [idx[0] for idx in sim]

    # 유사도 탑10 제목 가져오기
    # print(sim)                       # (인덱스, 유사도)
    return df.iloc[rec_idx]

df = pd.read_csv('book.csv')
cos_sim = np.load('sim.npy')
# ex = df.Title.sample(5)

# streamlit
st.title('독서는 마음의 양식')

title = st.text_input("책 제목을 입력해주세요")

# st.write(ex.values())

if title:
    ans = Recommend(title, cos_sim)
    ans.reset_index(drop = True, inplace = True)
     
    for i in range(5):
        st.subheader(ans.Title[i])
        col1, col2 = st.columns(2)
        with col1:
            st.image(ans.image[i], width = 200)
        with col2:
            st.write(ans.description[i][:400] + "   ...")
        st.header("")
