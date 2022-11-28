import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import sys

# 컴퓨터 메모리 부족으로 5천 권 까지만 학습
df = pd.read_csv("project_2.csv")
df = df[:5000]
print('전체 문서 개수 :', len(df))

corpus = [words.split() for words in df['description']]

word2vec_model = Word2Vec(corpus, vector_size = 300, window=5, min_count = 2, workers = -1)
# word2vec_model.build_vocab(corpus)
# word2vec_model.wv.vectors_lockf = np.ones(len(word2vec_model.wv), dtype=float)
# word2vec_model.wv.intersect_word2vec_format('GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)
# word2vec_model.train(corpus, total_examples = word2vec_model.corpus_count, epochs = 15)
word2vec_model.save('book_word2vector.model')

# 단어 벡터 평균 구하기
def get_document_vectors(document_list):
    document_embedding_list = []

    # 각 문서에 대해서
    for line in document_list:
        doc2vec = None
        count = 0
        for word in line.split():
            if word in word2vec_model.wv:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = word2vec_model.wv[word]
                else:
                    doc2vec = doc2vec + word2vec_model.wv[word]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list

document_embedding_list = get_document_vectors(df['description'])
print('문서 벡터의 수 :',len(document_embedding_list))

# 코사인 유사도 계산 후 저장
cosine_similarities = cosine_similarity(document_embedding_list, document_embedding_list)
print('코사인 유사도 매트릭스의 크기 :', cosine_similarities.shape)
np.save('book_cosine.npy', cosine_similarities)