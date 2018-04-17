# ! -*- coding:utf-8 -*-
import logging

import os
from gensim.models import doc2vec
from sklearn.decomposition import LatentDirichletAllocation

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

doc2vec_model_file = file_path() + '/../data/word2vecs/doc2vec_model.txt'


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
    vectors = doc2vec.Doc2Vec.load(doc2vec_model_file)
    get_items_by_LDA(vectors.docvecs.vectors_docs)