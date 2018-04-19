# ! -*- coding:utf-8 -*-
import logging

import numpy as np
import os
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src.Common.TextPreparer import TextPreparer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file_path = lambda: os.path.dirname(__file__)

model_path = file_path() + '/../data/models/classifier.m'

train_samples_path = file_path() + '/../data/classifier_data/words/train'
test_samples_path = file_path() + '/../data/classifier_data/words/test'


class Classifier(object):
    def create_model(self, train_samples, target_model):
        text_clf = Pipeline([('vec', CountVectorizer(lowercase=False, max_features=20)),
                             ('tfidf', TfidfTransformer(use_idf=False)),
                             ('clf', SVC())])

        text_clf.fit(train_samples['data'], train_samples['label'])
        joblib.dump(text_clf, target_model)
        return text_clf

    def test_model(self, test_samples, target_model, target_names):
        text_clf = joblib.load(target_model)
        predicted_data = text_clf.predict(test_samples['data'])
        print np.mean(test_samples['label'] == predicted_data)
        print metrics.classification_report(test_samples['label'], predicted_data, target_names=target_names)

    def get_sample_data_set(self, target_labels, train_sample_path):
        train_set = []
        for index, target_label in enumerate(target_labels):
            data_dir = os.path.join(train_sample_path, target_label)
            words, files = TextPreparer().combine_all_words(data_dir)
            train_set.extend(map(lambda x: (index, x), words))

        return train_set


if __name__ == '__main__':
    classifier = Classifier()
    target_labels = [u'other', u'国际形式', u'民生', u'革命']
    train_data_set = classifier.get_sample_data_set(target_labels, train_samples_path)
    test_data_set = classifier.get_sample_data_set(target_labels, test_samples_path)

    model = classifier.create_model({'data':[y for (x, y) in train_data_set], 'label': [x for (x, y) in train_data_set]}, model_path)
    classifier.test_model({'data': [y for (x, y) in test_data_set], 'label': [x for (x, y) in test_data_set]}, model_path, target_labels)

