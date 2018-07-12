from __future__ import unicode_literals, print_function, division

import re
import unicodedata
import random

from io import open

# 'This is a job.'
# ->
# word2index = {'SOS':0, 'EOS':1, 'This':2, 'is':3, 'a':4, 'job':5}
# word2count = {'This':1, 'is':1, 'a':1, 'job':1}
# index2word = {0:'SOS', 1:'EOS', 2:'This', 3:'is', 4:'a', 5:'job'}

SOS_token = 0
EOS_token = 1

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: 'SOS', 1: 'EOS'}
        self.n_words = 2

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]]+", r" ", s)
    return s

def readLangs(lang1, lang2, reverse = False):
    print('Reading lines ... ...')

    # Read the file and split into lines
    lines =  open('../resource/data/{0}-{1}.txt'.format(lang1, lang2), encoding='utf-8')\
        .read().strip().split('\n')

    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    # Revers pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs

MAX_LENGTH = 10

eng_prefixes = (
    "i am", "i m",
    "he is", "he s",
    "she is", "she s",
    "you are", "you re",
    "we are", "we re",
    "they are", "they re"
)

# not needed, just for effency
def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and \
           len(p[1].split(' ')) < MAX_LENGTH and \
           p[1].startswith(eng_prefixes)

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, reverse = False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("Read {0} sentence pairs".format(len(pairs)))
    pairs = filterPairs(pairs)
    print("Trimmed to {0} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])

    print("Counted words: ")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs

if __name__ == '__main__':
    input_lang, output_lang, pairs = prepareData('eng', 'fra', reverse=True)
    print(random.choice(pairs))
    # print('input_lang: ')
    # print(input_lang)
    # print('\n')
    # print('output_lang: ')
    # print(output_lang)
    # print('\n')
    # print('pairs: ')
    # print(pairs)



