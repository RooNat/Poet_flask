# -*-coding=utf-8-*-
'''
User:12433
Date:20220514
'''
from collections import Counter,defaultdict
import thulac
import jieba
import pickle
import os
import argparse
import json
import re
import jieba.posseg as pseg

import multiprocessing #多进程管理包
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def stopwordslist():
    stopwords=[]
    with open('data/json_zh/cn_stopwords.txt','r',encoding='utf-8') as f:
        line=f.readlines()
        for i in line:
            stopwords.append(i.strip())
    return stopwords

def poetdata(poetname,n):
    data_qts=[]
    word_list=[]
    stopwords=stopwordslist()
    # lex_analyzer = thulac.thulac()
    filename=''
    if n==1:
        filename='data/json_zh/poet_tang.json'
    else:
        filename='data/json_zh/ci_song.json'
    with open(filename,'r',encoding='utf-8') as f:
        obj=json.load(f)
        for i in obj:
            if i['author']==poetname:
                poem = ""
                for j in i['paragraphs']:
                    poem=poem+j
                data_qts.append(poem)
    word_counter = Counter()  # 词频统计
    for i in data_qts:
        valid_char_list = [c for c in i if '\u4e00' <= c <= '\u9fff' or c == '，' or c == '。']
        i=''.join(valid_char_list)
        line=jieba.cut_for_search(i)
        print("正在统计")
        for word in line:
            if word not in stopwords:
                word_list.append(word)
                word_counter[word]+=1
    print(dict(word_counter.most_common(10)))
    print(len(dict(word_counter)))
    if len(dict(word_counter))>=100:
        return dict(word_counter.most_common(100))
    else:
        length=len(dict(word_counter))
        return dict(word_counter.most_common(length))



if __name__ == '__main__':
    poetdata("李白",1)
