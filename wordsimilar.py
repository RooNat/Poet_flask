# -*-coding=utf-8-*-
'''
User:12433
Date:20220516
'''
from flask import Blueprint, render_template, request
from flask import jsonify
from process.word_level_analysis import tangmain
from process.word_level_song import songmain
from process.word_level_analysis_jieba import tangmainjieba
from process.word_level_song_jieba import songmainjieba

wordsimilar=Blueprint('wordsimilar',__name__)
filename=""
wordspath=""
filename1=""
wordspath1=""
filenamejie=""
wordspathjie=""
filenamejie2=""
wordspathjie2=""
@wordsimilar.route('/wordsimilar')
def wordpage():  # put application's code here
    return render_template("time_similar.html")

@wordsimilar.route('/wordfun')
def wordsimilarfun():
    data={}
    filename = 'data/json_zh/poet_tang.json'  # 唐
    wordspath = 'save_Skip1/tang_words_list.txt'
    char_counter, author_counter, genre_counter, vector_model = tangmain(filename, wordspath)

    #时间词
    time_count = dict(genre_counter['t'].most_common(10))
    time_data = []
    valdata = []
    for i, j in time_count.items():
        time_data.append({'name': i, 'value': j})
        valdata.append(j)
    data['tangtime'] = time_data
    data['tangmax'] = max(valdata)

    filename = 'data/json_zh/ci_song.json'  # 宋
    wordspath = 'save_Skip1/song_words_list.txt'
    char_counter, author_counter, genre_counter, title_counter, vector_model = songmain(filename, wordspath)

    #时间词
    time_count = dict(genre_counter['t'].most_common(10))
    time_data = []
    valdata = []
    for i, j in time_count.items():
        time_data.append({'name': i, 'value': j})
        valdata.append(j)
    data['songtime'] = time_data
    data['songmax'] = max(valdata)
    return jsonify(data)

@wordsimilar.route('/wordsimilarfun')
def similarsearch():
    data={}
    words = str(request.args.get('words'))
    radio=int(request.args.get('radiovalue'))
    #将jieba的文件移过来？？不用移过来，直接打开训练好的词向量
    #画雷达图 每个雷达图中含有唐宋
    #Thulac分词法
    # 唐
    global filename
    global wordspath
    global filename1
    global wordspath1
    global filenamejie
    global wordspathjie
    global filenamejie2
    global wordspathjie2
    print(radio)
    if radio==0:
        filename = 'data/json_zh/poet_tang.json'
        wordspath = 'save_CBOW1/tang_words_list.txt'

        filename1 = 'data/json_zh/ci_song.json'
        wordspath1 = 'save_CBOW1/song_words_list.txt'

        filenamejie = 'data/json_zh/poet_tang.json'
        wordspathjie = 'save_CBOW2/tang_words_list.txt'

        filenamejie2 = 'data/json_zh/ci_song.json'
        wordspathjie2 = 'save_CBOW2/song_words_list.txt'

    elif radio==1:
        print(radio)
        filename = 'data/json_zh/poet_tang.json'
        wordspath = 'save_Skip1/tang_words_list.txt'

        filename1 = 'data/json_zh/ci_song.json'
        wordspath1 = 'save_Skip1/song_words_list.txt'

        filenamejie = 'data/json_zh/poet_tang.json'
        wordspathjie = 'save_Skip2/tang_words_list.txt'

        filenamejie2 = 'data/json_zh/ci_song.json'
        wordspathjie2 = 'save_Skip2/song_words_list.txt'


    char_counter, author_counter, genre_counter, vector_model = tangmain(filename, wordspath)

    similar_words = dict(vector_model.wv.most_similar(words))
    wordname=[]
    wordvalue=[]
    for i,j in similar_words.items():
        wordname.append({'text':i,'max':1,'min':0.5})
        wordvalue.append(j)
    data['twordname_thu']=wordname
    data['twordvalue_thu']=wordvalue

    #宋

    char_counter, author_counter, genre_counter, title_counter, vector_model = songmain(filename1, wordspath1)

    similar_words = dict(vector_model.wv.most_similar(words))
    wordname = []
    wordvalue = []
    for i, j in similar_words.items():
        wordname.append({'text': i, 'max': 1,'min':0.5})
        wordvalue.append(j)
    data['swordname_thu'] = wordname
    data['swordvalue_thu'] = wordvalue
    print(data['swordvalue_thu'])

    #结巴分词器
    #唐

    char_counter, author_counter, genre_counter, vector_model = tangmainjieba(filenamejie, wordspathjie)

    similar_words = dict(vector_model.wv.most_similar(words))
    wordname = []
    wordvalue = []
    for i, j in similar_words.items():
        wordname.append({'text': i, 'max': 1,'min':0.5})
        wordvalue.append(j)
    data['twordname_jie'] = wordname
    data['twordvalue_jie'] = wordvalue

    # 宋

    char_counter, author_counter, genre_counter, title_counter, vector_model = songmainjieba(filenamejie2, wordspathjie2)

    similar_words = dict(vector_model.wv.most_similar(words))
    wordname = []
    wordvalue = []
    for i, j in similar_words.items():
        wordname.append({'text': i, 'max': 1,'min':0.5})
        wordvalue.append(j)
    data['swordname_jie'] = wordname
    data['swordvalue_jie'] = wordvalue
    print(data['swordvalue_jie'])

    return jsonify(data)