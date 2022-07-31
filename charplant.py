# -*-coding=utf-8-*-
'''
User:12433
Date:20220515
'''
from flask import Blueprint, render_template
from flask import jsonify
from process.word_level_analysis import tangmain
from process.word_level_song import songmain

charplant=Blueprint('charplant',__name__)

@charplant.route('/charplant')
def plantpage():  # put application's code here
    return render_template("char_plant.html")

@charplant.route('/charplantfun')
def plantfunction():
    data={}
    season=['春', '夏', '秋', '冬']  #季节
    plants = ['梅', '兰', '竹', '菊', '松', '柳', '枫', '桃', '梨', '杏', '莲']
    colors=[[['红','赤','丹','朱','彤','粉'],['橙', '缇'],['黄'],['棕','褐']],
            [['青','碧','翠'],['蓝'],['绿','沧','葱'],['紫','茈','堇']],
            [['白','素','皓','缥'],['黑','玄','乌','皂','黔','墨'],['灰']]]
    filename = 'data/json_zh/poet_tang.json'  #唐
    wordspath = 'save_Skip1/tang_words_list.txt'
    char_counter, author_counter, genre_counter, vector_model = tangmain(filename, wordspath)

    #季节
    season_count = []
    for a in season:
        season_count.append({'name': a, 'value': char_counter[a]})
        print(a, char_counter[a])  # ????!!!!!!!!!!!!!今天到这里
    data['tangseason'] = season_count
    #植物
    plant_count=[]
    for b in plants:
        plant_count.append({'name': b, 'value': char_counter[b]})
        print(b, char_counter[b])
    data['tangplant']=plant_count

    #颜色
    color_count={}
    for h in colors:
        for i in h:
            for j in i:
                color_count[j]=char_counter[j]
    data['tangcolor']=color_count

    filename = 'data/json_zh/ci_song.json'  #宋
    wordspath = 'save_Skip1/song_words_list.txt'
    char_counter, author_counter, genre_counter, title_counter, vector_model = songmain(filename, wordspath)

    #季节
    season_count = []
    for a in season:
        season_count.append({'name': a, 'value': char_counter[a]})
        print(a, char_counter[a])
    data['songseason'] = season_count

    #植物
    plant_count = []
    for b in plants:
        plant_count.append({'name': b, 'value': char_counter[b]})
        print(b, char_counter[b])
    data['songplant'] = plant_count

    #颜色
    color_count = {}
    for h in colors:
        for i in h:
            for j in i:
                color_count[j] = char_counter[j]
    data['songcolor'] = color_count


    return jsonify(data)