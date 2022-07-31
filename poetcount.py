# -*-coding=utf-8-*-
'''
User:12433
Date:20220514
'''
from flask import Blueprint, render_template
from flask import jsonify
from process.stconvert import  hant_2_hans
from process.stconvert import hans_2_hant
import sqlite3
import json
from process.word_level_analysis import tangmain
from process.word_level_song import songmain
poetcounts=Blueprint('poetcounts',__name__)


@poetcounts.route('/poetcounts')
def poetcountpage():  # put application's code here
    return render_template("poetcount.html")

@poetcounts.route('/poetcountroute',methods=['GET'])
def poetcount():
    data = {}
    conn = sqlite3.connect("data/cbdb_sqlite.db")
    c = conn.cursor()
    tang=open('data/json_zh/authors.tang.json','r',encoding='utf-8')
    song=open('data/json_zh/authors.songci.json','r',encoding='utf-8')
    tline=json.load(tang)
    sline=json.load(song)
    name_list=[]
    for i in tline:
        if i['name'] != '':
            t = hans_2_hant(i['name'])
            name_list.append(t)
    for i in sline:
        if i['name'] != '':
            s = hans_2_hant(i['name'])
            name_list.append(s)
    female=0
    male=0
    agepoet=[]
    agepoet.append(['Name','Age'])
    for j in name_list:
        sql = 'select c_female,c_death_age from BIOG_MAIN where c_name_chn=? and ((c_birthyear>=618 and c_birthyear<=907)\
        or (c_deathyear>=618 and c_deathyear<=907) or (c_birthyear>=960 and c_birthyear<=1279) or (c_deathyear>=960 and c_deathyear<=1279))'
        cursor = c.execute(sql, (j,))
        conn.commit()
        result = []
        for i in cursor:
            result.append(i)  # 包含性别和死时的年龄
        if len(result) != 0:
            if result[0][0]==0:
                male+=1
            elif result[0][0]==1:
                female+=1
            if result[0][1]!=None and result[0][1]!=0:
                agepoet.append([hant_2_hans(j),result[0][1]])

        data['age']=agepoet
        data['sex']=[]
        data['sex'].append({'name':'男','value':male})
        data['sex'].append({'name':'女','value':female})
    filename='data/json_zh/poet_tang.json'
    wordspath='save_Skip1/tang_words_list.txt'
    char_counter, author_counter, genre_counter, vector_model=tangmain(filename,wordspath)
    authorcount_tang=dict(author_counter.most_common(100))
    data['tang']=[]
    sumtang=0
    for i,j in authorcount_tang.items():
        data['tang'].append([i,j])
        sumtang+=j
    print(data['tang'])
    data['tangsum']=sumtang
    char_counter1, author_counter1, genre_counter1,title_counter,vector_model1 = songmain('data/json_zh/ci_song.json',
                                                                                          'save_Skip1/song_words_list.txt')
    authorcount_song = dict(author_counter1.most_common(100))
    data['song']=[]
    sumsong=0
    for i,j in authorcount_song.items():
        data['song'].append([i, j])
        sumsong+=j
    data['songsum']=sumsong
    print(data)
    return jsonify(data)