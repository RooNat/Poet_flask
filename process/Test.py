# -*-coding=utf-8-*-
'''
User:12433
Date:20220516
'''
from flask import Blueprint, render_template, request
from collections import Counter,defaultdict
from process.stconvert import  hant_2_hans
from process.stconvert import hans_2_hant
import sqlite3
import json
from flask import jsonify
from process.networks import SentimentAnalysis
from process.predict import predict
from process.Sentiment_Inference import *
import json
from process.word_single import stopwordslist
from process.word_single import poetdata
from process.word_level_analysis import tangmain
from process.word_level_song import songmain
import jieba.posseg as pseg

sentence="明月出天山，苍茫云海间。长风几万里，吹度玉门关。汉下白登道，胡窥青海湾。由来征战地，不见有人还。戍客望边色，思归多苦颜。高楼当此夜，叹息未应闲。"
vocab = set()  # 词汇库
word_counter = Counter()  # 词频统计
genre_counter = defaultdict(Counter)  # 针对每个词性的Counter
word_genre_pairs = pseg.cut(sentence)
word_list=[]
for word, genre in word_genre_pairs:  # 词频统计
    if word != '，' and word != '。':
        word_list.append(word)
        vocab.add(word)
        word_counter[word] += 1  # 词频统计
        genre_counter[genre][word] += 1  # 词性统计
wordgenre=[]
wordn=[]
wordns=[]
worda=[]
print(dict(genre_counter))
for i,j in dict(genre_counter).items():
    for h,r in dict(j).items():
        wordn.append({'name':h,'value':r})
    wordgenre.append({'name':i,'children':wordn})
print(word_list)
print(wordgenre)