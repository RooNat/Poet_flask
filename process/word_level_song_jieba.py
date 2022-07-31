# -*-coding=utf-8-*-
'''
User:12433
Date:20220507
'''


from collections import Counter,defaultdict
import thulac
import pickle
import os
import argparse
import json
import jieba
import jieba.posseg as pseg

import multiprocessing #多进程管理包
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


#用thulac进行分词
def cut_qts_to_words(qts_file,saved_words_file):
    save_dir=os.path.dirname((saved_words_file)) #返回文件路径
    dumped_file=os.path.join(save_dir,'song_words_start_result.pkl')

    if os.path.exists(dumped_file) and os.path.exists(saved_words_file):
        print('找到处理过的数据，正在加载...')
        with open(dumped_file,'rb') as f:
            char_counter, author_counter, vocab, word_counter, genre_counter,title_counter = pickle.load(f)
    else:
        char_counter=Counter()  #字频
        author_counter=Counter()  #作者作品数统计
        vocab=set() #词汇库
        word_counter=Counter() #词频统计
        genre_counter=defaultdict(Counter) #针对每个词性的Counter
        title_counter=Counter()

        fid_save=open(saved_words_file,'w',encoding='utf-8')#打开存储分词的文件
        #lex_analyzer=thulac.thulac()#分词器
        line_cnt=0

        obj=json.load(open(qts_file,'r',encoding='utf-8'))
        for d in obj:
            author=d['author']
            author_counter[author]+=1  #计算作者出现次数
            title=d['title'].split()
            title1=title[0]
            title_counter[title1]+=1
            poem1=d['paragraphs']#分出诗的部分
            #匹配所有中文
            poem=""
            for j in poem1:
                poem=poem+j

            valid_char_list = [c for c in poem if '\u4e00' <= c <= '\u9fff'or c == '，' or c == '。']
            for char in valid_char_list:
                char_counter[char] += 1
            regularized_poem = ''.join(valid_char_list)
            # 进行分词
            #word_genre_pairs = lex_analyzer.cut(regularized_poem)
            word_genre_pairs = pseg.cut(regularized_poem)
            word_list = []
            for word, genre in word_genre_pairs:  # 词频统计
                if word != '，' and word != '。':
                    word_list.append(word)
                    vocab.add(word)
                    word_counter[word] += 1  # 词频统计
                    genre_counter[genre][word] += 1  # 词性统计
            save_line = ' '.join(word_list)  # 保存每一行到新的分好词的文件里
            fid_save.write(save_line + '\n')

            if line_cnt % 10 == 0:
                print('%d poets processed.' % line_cnt)
            line_cnt += 1
        fid_save.close()
        # 存储下来
        # 将得到的数据保存下来
        dumped_data = [char_counter, author_counter, vocab, word_counter, genre_counter,title_counter]
        with open(dumped_file, 'wb') as f:
            pickle.dump(dumped_data, f)

    return char_counter, author_counter, genre_counter,title_counter

def word2vec(words_file):
    save_dir=os.path.dirname((words_file))
    #创建一个path来储存词向量
    vector_file=os.path.join(save_dir,'word_vectors_song.model')

    if os.path.exists(vector_file):
        print('找到词向量，正在加载...')
        model=Word2Vec.load(vector_file)
    else:
        print('计算词向量')
        model=Word2Vec(LineSentence(words_file),vector_size=400,window=8,min_count=10,sg=1,
                       workers=multiprocessing.cpu_count())
        model.save(vector_file)

    return model

def print_counter(counter):
    for k, v in counter:
        print(k, v)

def print_similar_words(word,vector_model):
    print('\n与"%s"比较意思比较接近的词' % word)
    print_counter(vector_model.wv.most_similar(word))

def print_stat_results(char_counter, author_counter, genre_counter, title_counter,vector_model):

    # 诗人写作数量排名
    print('\n诗人写作数量排名')
    print_counter(author_counter.most_common(10))
    # 基于字的分析
    print('\n\n基于字的分析')
    # 常用字排名
    print('\n常用字排名')
    print_counter(char_counter.most_common(12))

    print('\n词牌名使用排名')
    print_counter(title_counter.most_common(10))
    # 季节排名
    print('\n季节排名')
    for c in ['春', '夏', '秋', '冬']:
        print(c, char_counter[c])
        # 颜色排名
    print('\n颜色排名')
    colors = ['红', '白', '青', '蓝', '绿', '紫', '黑', '黄']
    for c in colors:
        print(c, char_counter[c])
    # 植物排名
    print('\n植物排名')
    plants = ['梅', '兰', '竹', '菊', '松', '柳', '枫', '桃', '梨', '杏','莲']
    for p in plants:
        print(p, char_counter[p])
    # 动物排名
    print('\n动物排名')
    age_animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    for a in age_animals:
        print(a, char_counter[a])
    # 基于词的分析
    print('\n\n基于词的分析')
    # 地名排名
    print('\n地名词排名')
    print_counter(genre_counter['ns'].most_common(16))
    # 时间排名
    print('\n时间词排名')
    print_counter(genre_counter['t'].most_common(10))
    # 场景排名
    print('\n场景词排名')
    print_counter(genre_counter['s'].most_common(10))

    print('\n形容词排名')
    print_counter(genre_counter['a'].most_common(10))

    #基于词向量的分析,用到了model
    print('\n\n基于词向量的分析')

    print_similar_words('天子',vector_model)
    print_similar_words('寂寞',vector_model)
    print(vector_model.wv.similarity('江北','寂寞'))

def songmainjieba(qts_path,words_path):
    # parser=argparse.ArgumentParser()
    # parser.add_argument('--qts_path', type=str, default='data/json_zh/ci_song.json',
    #                   help='file path of Songci')
    # #储存分词后的诗词word
    # parser.add_argument('--words_path', type=str, default='save_Skip1/song_words_list.txt',
    #                   help='file path to save_Skip1 Songci words data')
    # args=parser.parse_args()

    #检测储存目录是否存在
    save_dir=os.path.dirname(words_path)
    #如果不存在就创建目录
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    #分词，字计算，作者计算，词性计算
    char_counter,author_counter,genre_counter,title_counter=cut_qts_to_words(qts_path,words_path)

    #分词结果储存为词向量，下次不用重新计算
    vector_model=word2vec(words_path)

    # print_stat_results(char_counter,author_counter,genre_counter,title_counter,vector_model)
    return char_counter,author_counter,genre_counter,title_counter,vector_model

if __name__ == '__main__':
    filepath='../data/json_zh/ci_song.json'
    wordspath='../save_Skip2/song_words_list.txt'
    songmainjieba(filepath,wordspath)