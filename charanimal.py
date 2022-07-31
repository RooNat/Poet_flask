# -*-coding=utf-8-*-
'''
User:12433
Date:20220515
'''
from flask import Blueprint, render_template
from flask import jsonify
from process.word_single import stopwordslist
from process.word_level_analysis import tangmain
from process.word_level_song import songmain

charanimal=Blueprint('charanimal',__name__)

@charanimal.route('/charanimal')
def animalpage():  # put application's code here
    return render_template("char_animal.html")

@charanimal.route('/charanimalfun')
def animalfunction():
    data={}
    stopword=stopwordslist()
    age_animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

    filename = 'data/json_zh/poet_tang.json'
    wordspath = 'save_Skip1/tang_words_list.txt'
    char_counter, author_counter, genre_counter, vector_model=tangmain(filename,wordspath)
    animals_count=[]
    for a in age_animals:
        animals_count.append({'name':a,'value':char_counter[a]})
        print(a, char_counter[a])#????!!!!!!!!!!!!!今天到这里
    data['tanganimals']=animals_count
    char_count=dict(char_counter.most_common(300))
    char_data=[]
    for i,j in char_count.items():
        if i not in stopword:
            char_data.append({'name':i,'value':j})
    data['charword_tang']=char_data
    filename = 'data/json_zh/ci_song.json'
    wordspath = 'save_Skip1/song_words_list.txt'
    char_counter, author_counter, genre_counter,title_counter,vector_model = songmain(filename, wordspath)
    animals_count = []
    for a in age_animals:
        animals_count.append({'name': a, 'value': char_counter[a]})
        print(a, char_counter[a])
    data['songanimals'] = animals_count
    char_count = dict(char_counter.most_common(300))
    char_data = []
    for i, j in char_count.items():
        if i not in stopword:
            char_data.append({'name': i, 'value': j})
    data['charword_song'] = char_data

    return jsonify(data)