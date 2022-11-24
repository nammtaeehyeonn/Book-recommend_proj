import os, glob, json

root_dir = './data'
dic_file = root_dir + '/word-dic.json'
data_file = root_dir + '/data.json'
data_file_min = root_dir + '/data-mini.json'

word_dic = json.load(open(dic_file))
print(word_dic['_MAX'])
# for item in word_dic:
#    print(item)
