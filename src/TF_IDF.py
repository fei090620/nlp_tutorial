# ! -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os

from src.Common.FileProcessor import FileProcessor

file_path = lambda: os.path.dirname(__file__)

words_dir = file_path() + '/../data/words/'


class TF_IDF(object):
    def calculate_and_save_tf_idf_dict(self, words, tf_idf_path):
        vectorize =  CountVectorizer()


    # 合并所有词(不去重，去重了怎么统计词频？，去除空格,换行,空字符)
    def combine_all_words(self, words_dir):
        words = []
        files = os.listdir(words_dir)
        for file in files:
            single_words = [f.split(' ') for f in FileProcessor(os.path.join(words_dir, file)).file_read('utf8', '\n')]
            for word_list in single_words:
                words.extend(word_list)

        bool_list = [word is not u'' for word in words]
        return np.array(words)[bool_list]

if __name__ == '__main__':
    tf_idf = TF_IDF()
    words = tf_idf.combine_all_words(words_dir)
    for word in words:
        print word