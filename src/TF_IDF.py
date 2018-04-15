# ! -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
import os

from src.Common.FileProcessor import FileProcessor

file_path = lambda: os.path.dirname(__file__)

words_dir = file_path() + '/../data/words/'
tfidf_target_path = file_path() + '/../data/tfidf_vectors/'


class TF_IDF(object):
    def calculate_and_save_tf_idf_dict(self, words, tf_idf_path):
        vector =  CountVectorizer(lowercase=False)
        vector_matrix = vector.fit_transform(words)
        tfidf_matrix = TfidfTransformer(use_idf=False).fit_transform(vector_matrix)
        return tfidf_matrix

    # 合并所有词(不去重，去重了怎么统计词频？，去除空格,换行,空字符)
    def combine_all_words(self, words_dir):
        words = []
        files = os.listdir(words_dir)
        for file in files:
            single_words = FileProcessor(os.path.join(words_dir, file)).file_read('utf8', '\n')
            bool_list = [word is not u'' for word in single_words]
            words.append(u' '.join(np.array(single_words)[bool_list]))

        return words, files

    def save_tfidf_words_dict2files(self, tfidfs_list, target_path, files):
        length = len(files)
        for i in range(length):
            FileProcessor(os.path.join(target_path, files[i])).file_write('utf8', u' '.join([str(item) for item in tfidfs_list[i]]))
            print '{0}/{1}'.format(i, length)

if __name__ == '__main__':
    tf_idf = TF_IDF()
    words, files = tf_idf.combine_all_words(words_dir)
    tfidf_matrix = tf_idf.calculate_and_save_tf_idf_dict(words, '')
    print tfidf_matrix
    tf_idf.save_tfidf_words_dict2files(tfidf_matrix.toarray(), tfidf_target_path, files)