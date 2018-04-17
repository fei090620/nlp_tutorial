# ! -*- coding:utf-8 -*-
import logging

import matplotlib.pyplot as plt
import os
from gensim.models import doc2vec
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

doc2vec_model_file = file_path() + '/../data/word2vecs/doc2vec_model.txt'

map_file = file_path() + '/../data/word2vecs/tagged_map.txt'

def train_cluster_by_hierarchical(vectors, num_clusters=10):
    # scipy的层次聚类（可以获取聚类的过程）
    clusters_result = linkage(vectors, method='ward', metric='euclidean')

    #sklearn 层次聚类
    # hierachical = AgglomerativeClustering(n_clusters=num_clusters,
    #                                       affinity="euclidean",
    #                                       compute_full_tree=True,
    #                                       linkage='ward')

    return clusters_result

def show_cluster_progresses(cluster_result):
    plt.figure(figsize=(10, 8))
    dendrogram(cluster_result,
               truncate_mode='level',
               p=100,
               show_leaf_counts=True,
               leaf_rotation=90,
               leaf_font_size=12,
               show_contracted=True)
    plt.title('hierarchy tree')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    plt.show()

def show_cluster_samples_detail(vectors, cluster_labels):
    plt.figure(figsize=(10, 8))
    plt.title('cluster distribute status')
    plt.scatter(vectors[:, 0], vectors[:, 1], c=cluster_labels, cmap='prism')
    plt.show()


#根据聚类数目获取
def get_cluster_labels(cluster_result, cluster_num = 10):
    return fcluster(cluster_result, t=cluster_num, criterion='maxclust')


if __name__ == '__main__':
    vectors = doc2vec.Doc2Vec.load(doc2vec_model_file)
    vectors_docs = vectors.docvecs.vectors_docs
    clusters = train_cluster_by_hierarchical(vectors_docs)
    show_cluster_progresses(clusters)
    cluster_labels = get_cluster_labels(clusters)
    show_cluster_samples_detail(vectors_docs, cluster_labels)
