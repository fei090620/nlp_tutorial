# ! -*- coding:utf-8 -*-
import logging

import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from src.Common.FileProcessor import FileProcessor
from src.Common.TextPreparer import TextPreparer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


file_path = lambda: os.path.dirname(__file__)

words_dir = file_path() + '/../data/words/'
tfidf_target_path = file_path() + '/../data/tfidf_vectors/'


def calculate_and_save_tf_idf_dict(words_list):
    vector = CountVectorizer(lowercase=False)
    vector_matrix = vector.fit_transform(words_list)
    tfidf_matrix = TfidfTransformer(use_idf=False).fit_transform(vector_matrix)
    return tfidf_matrix


def save_tfidf_words_dict2files(tfidfs_list, target_path, files):
    length = len(files)
    for i in range(length):
        FileProcessor(os.path.join(target_path, files[i])).file_write('utf8', u' '.join([str(item) for item in tfidfs_list[i]]))
        print '{0}/{1}'.format(i, length)


if __name__ == '__main__':
    words_list, files = TextPreparer().combine_all_words(words_dir)
    tfidf_matrix = calculate_and_save_tf_idf_dict(words_list)
    print tfidf_matrix
    save_tfidf_words_dict2files(tfidf_matrix.toarray(), tfidf_target_path, files)