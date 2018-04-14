# ! -*- coding:utf-8 -*-

import os
import codecs
import re

import jieba
import numpy as np

texts_dir = './data/news/'
sentences_file_dir_path = './data/sentences/'
stop_words_file = './data/stop_words.txt'
similar_words_file = './data/similar_v2.txt'


# 获取数据
def get_files_texts(file_dir):
    file_names = os.listdir(texts_dir)
    text_path_list = [os.path.join(file_dir, f) for f in file_names]
    texts = []
    for file_path in text_path_list:
        f = codecs.open(file_path,'r','utf8')
        texts.append(f.read())
        f.close()
    return file_names, texts

# 断句
def cut_to_sentences(file_names, texts, target_dir):
    split_pattern = u"【|】|，|。|？|！|：|“|、|_|”| |-"
    sub_pattern = u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"

    for i in range(len(texts)):
        sentences = re.split(split_pattern, texts[i])
        result_sentences = [re.sub(sub_pattern, '', sentence) for sentence in sentences]
        file_with_sentence = os.path.join(target_dir, file_names[i])
        print file_with_sentence

        f = codecs.open(file_with_sentence, 'w', 'utf8')
        f.writelines(u'\n'.join(result_sentences))
        f.close()

# 去除停用词（网络常用词库）
def filter_by_stop_words(words):
    file = codecs.open(stop_words_file, 'r', 'utf-8')
    stop_words = file.readlines()
    file.close()
    bool_list = np.logical_not([word in stop_words for word in words])
    return np.array(words)[bool_list]


# 处理近义词（哈工大词库）


# 分词
def cut_words(text_file):
    file = codecs.open(text_file, 'r', 'utf8')
    sentences = file.readlines()
    for sentence in sentences:
        original_cut_words = jieba.lcut(sentence, cut_all=False, HMM=False)



if __name__ == '__main__':
    files, texts = get_files_texts(texts_dir)
    for (file, text) in zip(files, texts):
        print file, text

    cut_to_sentences(files, texts, sentences_file_dir_path)
