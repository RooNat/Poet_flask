# -*-coding=utf-8-*-
'''
User:12433
Date:20220515
'''
from flask import Blueprint, render_template, request
from collections import Counter,defaultdict
from process.stconvert import  hant_2_hans
from process.stconvert import hans_2_hant
import sqlite3
import json
from flask import jsonify
from process.word_single import stopwordslist
from process.word_single import poetdata
from process.word_level_analysis import tangmain
from process.word_level_song import songmain

locword=Blueprint('locword',__name__)

@locword.route('/locword')
def locwordpage():  # put application's code here
    return render_template("location_word.html")

@locword.route('/locwordfun')
def locwordfunction():
    data={}
    filename = 'data/json_zh/poet_tang.json'  # 唐
    wordspath = 'save_Skip1/tang_words_list.txt'
    locationjson='data/json_zh/location.json'
    longdata = []
    aldata=[]
    char_counter, author_counter, genre_counter, vector_model = tangmain(filename, wordspath)
    f=open(locationjson,'r',encoding='utf-8')
    line=json.load(f)

    #场景词
    loc_count = dict(genre_counter['s'].most_common(10))
    loc_data = []
    valdata=[]
    for i, j in loc_count.items():
        loc_data.append({'name': i, 'value': j})
        valdata.append(j)
    data['tangloc'] = loc_data
    data['tangmax'] = max(valdata)

    # 地点词
    site_count = dict(genre_counter['ns'].most_common(12))
    site_data = []
    for i, j in site_count.items():
        for h in line:
            if i==h['name']:
                site_data.append([h['longitude'],h['latitude'],j,i,h['loc'],h['img']])
                longdata.append(h['longitude'])
                aldata.append(h['latitude'])
                break
    data['sitetang'] = site_data
    # data['tangmax'] = max(valdata)


    # 宋
    filename = 'data/json_zh/ci_song.json'
    wordspath = 'save_Skip1/song_words_list.txt'
    char_counter, author_counter, genre_counter, title_counter, vector_model = songmain(filename, wordspath)


    # 场景词
    loc_count = dict(genre_counter['s'].most_common(10))
    loc_data = []
    valdata = []
    for i, j in loc_count.items():
        loc_data.append({'name': i, 'value': j})
        valdata.append(j)
    data['songloc'] = loc_data
    data['songmax'] = max(valdata)

    #词牌名
    title_count=dict(title_counter.most_common(20))
    titlename=[]
    titlenum=[]
    for i,j in title_count.items():
        titlename.append(i)
        titlenum.append(j)

    data['titlename']=titlename
    data['titlenum']=titlenum

    #地点词
    site_count = dict(genre_counter['ns'].most_common(16))
    site_data = []
    for i, j in site_count.items():
        for h in line:
            if i == h['name']:
                site_data.append([h['longitude'], h['latitude'], j, i, h['loc'],h['img']])
                longdata.append(h['longitude'])
                aldata.append(h['latitude'])
                break
    data['sitesong'] = site_data
    data['longmax']=max(longdata)
    data['almax']=max(aldata)
    data['longmin']=min(longdata)
    data['almin']=min(aldata)
    print(data['sitetang'])
    print(data['sitesong'])
    print(longdata)
    print(data['longmax'])

    return jsonify(data)