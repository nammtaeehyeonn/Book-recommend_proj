import streamlit as st
import numpy as np
import pandas as pd


# 타이틀 설정
st.title("책 제목을 통한 유사 도서 추천")

st.text_input("책 제목을 입력해주세요")

if st.button("검색"):
    st.write("유사 도서 제목을 출력합니다.")

from PIL import Image

image = Image.open("img.jpg")

st.image(image)
