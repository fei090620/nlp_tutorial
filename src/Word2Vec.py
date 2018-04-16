# ! -*- coding:utf-8 -*-
import logging

import os
from gensim.models import doc2vec
from gensim.models.doc2vec import TaggedLineDocument

from src.Common.FileProcessor import FileProcessor
from src.Common.TextPreparer import TextPreparer

file_path = lambda: os.path.dirname(__file__)

words_dir = file_path() + '/../data/words/'
word2vec_taget_dir = file_path() + '/../data/word2vecs/'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Word2Vec(object):
    def calculate_and_save_word2vec_dict(self, words_list, files):
        dataset_file = os.path.join(word2vec_taget_dir, 'dataset.txt')
        FileProcessor(dataset_file).file_write('utf8', u''.join([words + u'\n' for words in words_list][:-1]))
        doces = TaggedLineDocument(dataset_file)

        doc2Vec_model = doc2vec.Doc2Vec(doces, size=200, window=10, workers=4)
        doc2Vec_model.train(doces, total_examples=doc2Vec_model.corpus_count, epochs=100)
        doc2Vec_model.save(os.path.join(word2vec_taget_dir, 'doc2vec_model.txt'))
        FileProcessor(os.path.join(word2vec_taget_dir, 'tagged_map.txt'))\
            .file_write('utf8', u''.join([u'{0} {1} \n'.format(index,value.decode('utf8')) for index, value in enumerate(files)]))

        return doc2Vec_model


if __name__ == '__main__':
    words_list, files = TextPreparer().combine_all_words(words_dir)
    Word2Vec().calculate_and_save_word2vec_dict(words_list, files)