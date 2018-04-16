# coding=utf-8

# 数据准备
import numpy as np
import os
import re

import jieba.posseg as psg

from src.Common.FileProcessor import FileProcessor


class TextPreparer(object):
    def cut2sentences(self, text):
        split_pattern = u"【|】|，|。|？|！|：|“|、|_|”| |-|；"
        sub_pattern = u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）△]+"
        sentences = re.split(split_pattern, text)
        return [re.sub(sub_pattern, '', sentence) for sentence in sentences]

    def saveSentences2file(self, target_dir, file_name, sentences):
        file = os.path.join(target_dir, file_name)
        FileProcessor(file).file_writeLines('utf8', u'\n'.join(sentences))
        return file

    def saveWords2file(self, target_dir, file_name, words_list):
        file = os.path.join(target_dir, file_name)
        FileProcessor(file).file_writeLines('utf8', u'\n'.join([u' '.join(words) for words in words_list]))
        return file

    # 句子分词并且标记
    def cutSentence2Words_with_tagged(self, sentences, stop_words, similar_words):
        tagged_words_list = []
        for sentence in sentences:
            original_cut_words = psg.lcut(sentence, HMM=False)
            filter_stop_words = self.filter_by_stop_words(original_cut_words, stop_words)
            tagged_words = self.pos_sense_tagged(filter_stop_words, similar_words)
            tagged_words_list.append(tagged_words)

        return tagged_words_list

    # 句子分词，并替换同义词
    def cutSentence2Words_without_tagged(self, sentences, stop_words, similar_words):
        words_list = []
        for sentence in sentences:
            original_cut_words = psg.lcut(sentence, HMM=False)
            filter_stop_words = self.filter_by_stop_words(original_cut_words, stop_words)
            cut_words = self.replace_with_similar_wrods(filter_stop_words, similar_words)
            words_list.append(cut_words)

        return words_list

    # 去除停用词
    def filter_by_stop_words(self, words, stop_words):
        bool_list = np.logical_not([word.word in stop_words for word in words])
        return np.array(words)[bool_list]

    # 处理近义词和相关词（哈工大词库）做标注（词性和词义）
    def pos_sense_tagged(self, words, similar_words):
        tagged_words = []
        for w in words:
            target_list = (line.split(' ')[0] if w.word in line.split(' ')[1:]
                         else ''
                         for (index, line) in enumerate(similar_words))
            tagged_words.append(u'/'.join([w.word, w.flag, reduce(lambda x, y: x or y, target_list or [u'@'])]))

        return tagged_words

    #处理近义词，替换
    def replace_with_similar_wrods(self, words, similar_words):
        replaced_words = []
        for w in words:
            target_list = (line.split(' ')[-1] if w.word in line.split(' ')[1:] and line.split(' ')[0][-1] == u'='
                         else ''
                         for (index, line) in enumerate(similar_words))
            replaced_words.append(reduce(lambda x, y: x or y, target_list) or w.word)

        return replaced_words

    # 合并所有词(不去重，去重了怎么统计词频？，去除空格,换行,空字符)
    def combine_all_words(self, words_dir):
        words = []
        files = os.listdir(words_dir)
        for file in files:
            single_words = FileProcessor(os.path.join(words_dir, file)).file_read('utf8', '\n')
            bool_list = [word is not u'' for word in single_words]
            words.append(u' '.join(np.array(single_words)[bool_list]))

        return words, files


