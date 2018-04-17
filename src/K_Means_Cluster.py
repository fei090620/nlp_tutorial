import logging

import os
from gensim.models import doc2vec
from sklearn.cluster import KMeans

from src.Common.FileProcessor import FileProcessor

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

doc2vec_model_file = file_path() + '/../data/word2vecs/doc2vec_model.txt'

map_file = file_path() + '/../data/word2vecs/tagged_map.txt'


def save_label_to_tagged_file(cluster_result, tagged_file):
    file_processor = FileProcessor(tagged_file)
    samples = file_processor.file_read('utf8', u'\n')
    cluster_samples = [u'{0} {1}\n'.format(sample, label) for (sample, label) in zip(samples, cluster_result)]
    file_processor.file_write('utf8', u''.join(cluster_samples))


def train_cluster(vectors, num_cluster=10):
    km = KMeans(n_clusters=num_cluster, n_jobs=1)
    cluster_result = km.fit_predict(vectors.docvecs.vectors_docs)
    return cluster_result


if __name__ == '__main__':
    vectors = doc2vec.Doc2Vec.load(doc2vec_model_file)
    clusters = train_cluster(vectors)
    save_label_to_tagged_file(clusters, map_file)





