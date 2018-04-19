# ! -*- coding:utf-8 -*-
import logging

import numpy as np
import os

from src.Common.FileProcessor import FileProcessor
from src.Common.TextPreparer import TextPreparer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

lables_file_path = file_path() + '/../data/labels.txt'
classifier_words_train_data_path = file_path() + '/../data/classifier_data/words/train/'
classifier_words_test_data_path = file_path() + '/../data/classifier_data/words/test/'
sample_words_dir = file_path() + '/../data/words/'

class MarkLablesbyKeyWords(object):
    def __init__(self, labels):
        self.labels = labels

    def mkdirforLables(self, target_path):
        other_dir = os.path.join(target_path, u'other')
        if not os.path.exists(other_dir):
            os.makedirs(other_dir)

        labels_dirs = []
        for label, values in self.labels.items():
            label_dir = os.path.join(target_path, label)
            if not os.path.exists(label_dir):
               os.makedirs(label_dir)
            labels_dirs.append(label_dir)
        return labels_dirs

    def moveSampleWordsToLableDir(self, sample_words_file_dir, dist_dir_path):
        words_list, files = TextPreparer().combine_all_words(sample_words_file_dir)
        file_lables = []
        for words in words_list:
            label_list = [x if len(np.intersect1d(words.split(u' '), y)) else u'' for (x, y) in self.labels.items()]
            file_lables.append(filter(lambda x: x, label_list) or [u'other'])

        for (index, file_label) in enumerate(file_lables):
            dist_dirs = [os.path.join(dist_dir_path, label) for label in file_label]
            bool_list = [os.path.exists(dir_item) for dir_item in dist_dirs]
            effect_dist_dirs = np.array(dist_dirs)[bool_list]
            for dist_dir in effect_dist_dirs:
                FileProcessor(os.path.join(sample_words_file_dir, files[index]))\
                    .file_copy(os.path.join(dist_dir, files[index].decode('utf8')))


if __name__ == '__main__':
    labels = FileProcessor(lables_file_path).file_read('utf8', u'\n')[1:]
    labels_dict = dict([(x.split(u' ')[0], x.split(u' ')[1].split('\\')) for x in labels])
    for index, value in labels_dict.items():
        print index, u' '.join(value)

    marker = MarkLablesbyKeyWords(labels_dict)
    marker.mkdirforLables(classifier_words_train_data_path)
    marker.mkdirforLables(classifier_words_test_data_path)
    marker.moveSampleWordsToLableDir(sample_words_dir, classifier_words_train_data_path)

