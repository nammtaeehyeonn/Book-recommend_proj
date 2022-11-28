from gensim.models import word2vec
data = word2vec.Text8Corpus("../data/wiki.wakati")
model = word2vec.Word2Vec(data, vector_size=100) # 길이 100으로 설정
model.save("../data/wiki.model")
print("ok")
