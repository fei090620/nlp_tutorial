# ! -*- coding:utf-8 -*-
import logging

import os
from sklearn.decomposition import LatentDirichletAllocation

from src.WordVector.TF_IDF import load_tfidf_matrix

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

doc2vec_model_file = file_path() + '/../data/word2vecs/doc2vec_model.txt'

tfidf_target_path = file_path() + '/../data/tfidf_vectors/'


# 使用LDA主题抽取算法进行计算
def get_items_by_LDA(doc_vectors, n_topics=10):
    lda_model = LatentDirichletAllocation(n_topics=n_topics,
                                          max_iter=100,
                                          learning_method='online',
                                          learning_offset=50.,
                                          random_state=0)
    lda_model.fit(doc_vectors)
    return lda_model

if __name__ == '__main__':
    vectors = load_tfidf_matrix(tfidf_target_path)
    lda_model = get_items_by_LDA(vectors)