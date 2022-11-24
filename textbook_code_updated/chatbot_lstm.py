import random, os, sys, json, re, glob, codecs
import numpy as np
import tensorflow as tf
from bs4 import BeautifulSoup
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Activation, LSTM
from tensorflow.keras.optimizers import RMSprop

data_dir = './dialogue'
for dir in os.listdir(data_dir):
    dir_path = data_dir + '/' + dir
    if not os.path.isdir(dir_path): continue
    files = glob.glob(dir_path + '/*.txt')
    for file in files:
        with open(file, 'r') as f:
            text = f.read()
            text = re.sub('^[0-9] : ', '', text, flags=re.MULTILINE)
            # print(text[:100])
            # sys.exit(0)

            # 문자를 하나하나 읽어들이고 ID 붙이기
            chars = sorted(list(set(text)))
            print('사용되고 있는 문자 수: ', len(chars))
            char_indices = dict((c, i) for i, c in enumerate(chars)) # 문자 -> ID
            indices_char = dict((i, c) for i, c in enumerate(chars)) # ID -> 문자            
            print(char_indices)





# fp = codecs.open('data/BEXX0003.txt', encoding='utf-16')
# soup = BeautifulSoup(fp, 'html.parser')
# body = soup.select_one('body')
# text = body.getText() + ' '
# print('코퍼스 길이: ', len(text))

# # 문자를 하나하나 읽어들이고 ID 붙이기
# chars = sorted(list(set(text)))
# print('사용되고 있는 문자 수: ', len(chars))
# char_indices = dict((c, i) for i, c in enumerate(chars)) # 문자 -> ID
# indices_char = dict((i, c) for i, c in enumerate(chars)) # ID -> 문자

# # 텍스트를 maxlen 개의 문자로 자르고 다음에 오는 문자 등록하기
# maxlen = 20
# step = 3
# sentences = []
# next_chars = []
# for i in range(0, len(text) - maxlen, step):
#     sentences.append(text[i: i + maxlen])
#     next_chars.append(text[i + maxlen])
# print('학습할 구문의 수: ', len(sentences))
# print('텍스트를 ID 벡터로 변환합니다....')
# X = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
# y = np.zeros((len(sentences), len(chars)), dtype=bool)
# for i, sentence in enumerate(sentences):
#     for t, char in enumerate(sentence):
#         X[i, t, char_indices[char]] = 1
#     y[i, char_indices[next_chars[i]]] = 1

# print('x shape=', X.shape)
# # LSTM 모델 구축 
# print('모델을 구축합니다.')
# #model = Sequential()
# #model.add(LSTM(128, input_dim=maxlen * len(chars)))
# #model.add(Dense(len(chars)))
# #model.add(Activation('softmax'))
# model = Sequential([
#     Input(shape=(maxlen, len(chars))),
#     LSTM(128),
#     Dense(len(chars), activation='softmax')
#     ])
# optimizer = RMSprop(learning_rate=0.01)
# model.compile(loss='categorical_crossentropy', optimizer=optimizer)

# # 후보를 배열에서 꺼내기
# def sample(preds, temperature=1.0):
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)
#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)

# # 학습 생성 반복
# for iteration in range(1, 60):
#     print()
#     print('-' * 50)
#     print('반복=', iteration)
#     model.fit(X, y, batch_size=128, epochs=1)
    
#     # 임의의 시작 텍스트 선택
#     start_index = random.randint(0, len(text) - maxlen - 1)

#     # 다양한 문장 생성
#     for diversity in [0.2, 0.5, 1.0, 1.2]:
#         print()
#         print('---다양성 = ', diversity)
#         generated = ''
#         sentence = text[start_index: start_index + maxlen]
#         generated += sentence
#         print(f'---시드 = "{sentence}"')
#         sys.stdout.write(generated)
#         # 시드를 기반으로 텍스트 자동 생성
#         for i in range(400):
#             x = np.zeros((1, maxlen, len(chars)))
#             for t, char in enumerate(sentence):
#                 x[0, t, char_indices[char]] = 1.
#             # 다음에 올 문자 예측
#             preds = model.predict(x, verbose=0)[0]
#             next_index = sample(preds, diversity)
#             next_char = indices_char[next_index]
#             # 출력
#             generated += next_char
#             sentence = sentence[1:] + next_char
#             sys.stdout.write(next_char)
#             sys.stdout.flush()
#         print()


