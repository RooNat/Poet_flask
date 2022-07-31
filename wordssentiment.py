# -*-coding=utf-8-*-
'''
User:12433
Date:20220516
'''
from flask import Blueprint, render_template, request
from collections import Counter,defaultdict
from flask import jsonify
from process.networks import SentimentAnalysis
from process.predict import predict
from process.Sentiment_Inference import Sentiment_Analysis

SA = SentimentAnalysis()

import jieba.posseg as pseg

wordssentiment=Blueprint('wordssentiment',__name__)

@wordssentiment.route('/wordssentiment')
def wordsentimentpage():  # put application's code here
    return render_template("sentiment.html")

@wordssentiment.route('/wordssentimentfun')
def sentimentfunction():
    data={}
    sentence = str(request.args.get('sentence'))
    #情感分析
    #基于情感词典的情感分析
    pos, neg = SA.normalization_score(sentence)
    label = predict(sentence)
    if label==1:
        label="正向"
    elif label==0:
        label="中性"
    else:
        label="负向"
    # 基于BERT的情感分析
    model=Sentiment_Analysis(max_seq_len=170, batch_size=1)
    databert=model(sentence)
    print(databert)
    data['sentiment_dic']=[{'pos':pos,'neg':neg,'label':label}]
    data['databert']=databert
    if data['databert'][0]['pred']>data['databert'][0]['threshold']:
        data['bertlabel']="积极向"
    elif data['databert'][0]['pred']==data['databert'][0]['threshold']:
        data['bertlabel'] = "中性"
    else:
        data['bertlabel']="消极向"

    #词频统计
    #jieba
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
    # wordn=[]
    wordns=[]
    worda=[]
    jiebagenre=open('data/json_zh/jiebagenre.txt','r',encoding='utf-8')
    lines=jiebagenre.readlines()
    print(dict(genre_counter))
    for i, j in dict(genre_counter).items():
        wordn=[]
        for h, r in dict(j).items():
            wordn.append({'name': h, 'value': r})
        for s in lines:
            s.strip()
            s=s.replace('\n','')
            textarg=s.split()
            if textarg[0]==i:
                wordgenre.append({'name': s, 'children': wordn})
                break
    data['treedata']=wordgenre
    print(data['treedata'])
    return jsonify(data)


