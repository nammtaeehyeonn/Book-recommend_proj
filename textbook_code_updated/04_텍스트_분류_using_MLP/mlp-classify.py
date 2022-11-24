import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from scikeras.wrappers import KerasClassifier
from tensorflow.keras.utils import to_categorical 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json

print('텐서플로 버전: ', tf.__version__)

max_words = 56681
nb_classes = 6 

batch_size = 64 
nb_epoch = 10

# MLP 모델 생성
def build_model():
    model = Sequential()
    model.add(Dense(512, input_dim=max_words))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])
    return model

# 데이터 로드
data = json.load(open('../data/data-mini.json'))
# data = json.load(open('./data/data.json'))
X = np.array(data['X']) # 텍스트 데이터
Y = np.array(data['Y']) # 카테고리 데이터 (132,) 2차원 배열

print('X shape: ', X.shape)
print('y 클래스=', np.unique(Y))
print('y shape: ', Y.shape)

# 학습
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
Y_train = to_categorical(Y_train, nb_classes) # 6열로 원핫 인코딩
print('Y_train shape=', Y_train.shape) # Y_test는 1열 그대로 사용

model = KerasClassifier(model=build_model,
                        epochs=nb_epoch,
                        batch_size=batch_size)
model.fit(X_train, Y_train)

# 예측
pred = model.predict(X_test).argmax(axis=1) # 예측값이 6열로 반환되어 가장 큰 값 1개만 출력
print('pred shape=', pred.shape) 
print('pred[0]=', pred[0])

ac_score = accuracy_score(Y_test, pred)
cl_report = classification_report(Y_test, pred)
print('정답률: ', ac_score)
print('리포트:\n', cl_report)

print(model.target_encoder)
print(model.target_encoder_)
