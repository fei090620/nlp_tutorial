# ! -*- coding:utf-8 -*-

import time

import codecs
import os

from Common.FileProcessor import FileProcessor
from Common.TextPreparer import TextPreparer

file_path = lambda: os.path.dirname(__file__)

texts_dir = file_path() + '/../data/news/'
sentences_file_dir_path = file_path() + '/../data/sentences/'
stop_words_file = file_path() + '/../data/stop_words.txt'
similar_words_file = file_path() + '/../data/similar_v2.txt'
tagged_words_dir = file_path() + '/../data/tagged_words/'
words_dir = file_path() + '/../data/words/'


# 获取原始数据
def get_files_texts(file_dir):
    file_names = os.listdir(texts_dir)
    text_path_list = (os.path.join(file_dir, f) for f in file_names)
    texts = []
    for file_path in text_path_list:
        with codecs.open(file_path, 'r', 'utf8') as f:
            texts.append(f.read())

    return file_names, texts


def cut_save_sentences(files, texts, sentences_file_dir_path, textPreparer):
    for i in range(len(texts)):
        # 如果文件已存在，不重复处理
        if os.path.exists(os.path.join(sentences_file_dir_path, files[i])):
            continue

        # 计时开始
        start = time.clock()
        # 断句
        result_sentences = textPreparer.cut2sentences()
        textPreparer.saveSentences2file(sentences_file_dir_path, files[i], result_sentences)
        # 计时结束
        end = time.clock() - start
        # 打印当前进度
        print u'断句：', u'{0}/{1}'.format(i + 1, len(texts)), str(end)


def cut_save_tagged_words(files, sentences_file_dir_path, textPreparer, tagged_words_dir):
    for i in range(len(files)):
        # 如果文件已存在，不重复处理
        if os.path.exists(os.path.join(tagged_words_dir, files[i])):
            print u'{0}/{1}'.format(i + 1, len(texts)), u'存在'
            continue

        # 计时开始
        start = time.clock()

        # load 短语，时间换空间
        # sentences = FileProcessor(os.path.join(sentences_file_dir_path, files[i])).file_read('utf8', '\n')
        sentences = FileProcessor(os.path.join(sentences_file_dir_path, files[i])).file_read_iterator('utf8', '\n')

        # 分词标记
        tagged_words_list = textPreparer.cutSentence2Words_with_tagged(sentences, stop_words, hgd_similar_words)
        textPreparer.saveWords2file(tagged_words_dir, files[i], tagged_words_list)

        # 计时结束
        end = time.clock() - start
        # 打印当前进度
        print u'标记分词：', u'{0}/{1}'.format(i + 1, len(texts)), str(end)

def cut_save_words(files, sentences_file_dir_path, textPreparer, words_dir):
    for i in range(len(files)):
        # 如果文件已存在，不重复处理
        if os.path.exists(os.path.join(words_dir, files[i])):
            print u'{0}/{1}'.format(i + 1, len(texts)), u'存在'
            continue

        # 计时开始
        start = time.clock()

        # load 短语，时间换空间
        sentences = FileProcessor(os.path.join(sentences_file_dir_path, files[i])).file_read_iterator('utf8', '\n')

        # 分词不标记
        words_list = textPreparer.cutSentence2Words_without_tagged(sentences, stop_words, hgd_similar_words)
        textPreparer.saveWords2file(words_dir, files[i], words_list)

        # 计时结束
        end = time.clock() - start
        # 打印当前进度
        print u'不标记分词：', u'{0}/{1}'.format(i + 1, len(texts)), str(end)


if __name__ == '__main__':
    files, texts = get_files_texts(texts_dir)
    stop_words = FileProcessor(stop_words_file).file_read('utf8', '\n')
    hgd_similar_words = FileProcessor(similar_words_file).file_read('gbk', '\r\n')
    textPreparer = TextPreparer()
    cut_save_sentences(files, texts, sentences_file_dir_path, textPreparer)
    cut_save_tagged_words(files, sentences_file_dir_path, textPreparer, tagged_words_dir)
    cut_save_words(files, sentences_file_dir_path, textPreparer, words_dir)






