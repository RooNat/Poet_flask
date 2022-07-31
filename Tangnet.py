# -*-coding=utf-8-*-
'''
User:12433
Date:20220517
'''
from flask import Blueprint, render_template, request
from process.stconvert import  hant_2_hans
from flask import jsonify
import pickle
import math

Tangnet=Blueprint('Tangnet',__name__)

@Tangnet.route('/Tangnet')
def Tangnetpage():  # put application's code here
    return render_template("Tangnet.html")


# 直接获取排名前visulize_range的引用关系
def get_concerned_relations_by_range(reference_relations_counter, visulize_range):
  # 获取引用关系
  relations = reference_relations_counter.most_common(visulize_range)
  max_refer_count = relations[0][1]
  min_refer_count = relations[-1][1]

  return relations, max_refer_count, min_refer_count

# 获取指定诗人群体之间的引用关系，适合画出某个群体内部的网络
def get_concerned_relations_by_authors(reference_relations_counter, authors):
  # 获取指定作者群体内部的引用关系
  relations = []
  max_refer_count = 0
  min_refer_count = 10000
  for (refered_by, refered), count in reference_relations_counter.items():
    # 不统计自引用的count
    if refered_by == refered:
      continue
    if refered_by in authors and refered in authors:
      if count > max_refer_count:
        max_refer_count = count
      if count < min_refer_count:
        min_refer_count = count

      relations.append(((refered_by, refered), count))

  return relations, max_refer_count, min_refer_count

def get_data_links_tang(relations,max_refer_count,min_refer_count,count_to_plot_threshold=1):
    min_link_width = 0.5
    max_link_width = 5.0

    # 因为引用关系的强弱范围很大，对其开方降低变化范围，画图更直观
    max_refer_count = math.sqrt(max_refer_count)
    min_refer_count = math.sqrt(min_refer_count)
    width_slope = (max_link_width - min_link_width) / (max_refer_count - min_refer_count)

    links=[]
    # links_item_format = """{source: '%s', target: '%s',
    #   lineStyle:{normal:{width: %f}}},
    #   """

    filtered_authors=set()
    for (refered_by,refered),count in relations:
        #跳过自引用，不然有可能画出孤立节点
        if refered_by==refered:
            continue
            # 小于门限跳过
        if count < count_to_plot_threshold:
            continue
        filtered_authors.add(refered_by)
        filtered_authors.add(refered)
        num=count
        count = math.sqrt(count)
        line_width = min_link_width + width_slope * (count - min_refer_count)
        links.append({'source':hant_2_hans(refered_by),'target':hant_2_hans(refered),'lineStyle':{'normal':{'width':line_width},'value':num,'tooltip':{'formatter':'{c}'}}})

    datanode=[]
    d = 4
    for author in filtered_authors:
        files_name_array = [('data/json_zh/early_tang_poets.txt', 0), ('data/json_zh/high_tang_poets.txt', 1),
                            ('data/json_zh/middle_tang_poets.txt', 2), ('data/json_zh/late_tang_poets.txt', 3)]
        for authors_file_path, num in files_name_array:
            with open(authors_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            authors = set(text.split())
            if author in authors:
                d = num
                break
        author_count=0
        for (refered_by,refered),count in relations:
            if author==refered_by or author==refered:
                author_count+=1
        datanode.append({'name':hant_2_hans(author),'value':author_count,'symbolSize':author_count*3,'category':d})

    return links,datanode

# 有些时候如果画出所有关系会显得非常拥挤，用count_to_plot_threshold来控制最小显示出来的关系
# 只有引用数大于等于count_to_plot_threshold的关系才会显示出来
def get_data_links(relations,max_refer_count,min_refer_count,count_to_plot_threshold=1):
    min_link_width = 0.5
    max_link_width = 5.0

    # 因为引用关系的强弱范围很大，对其开方降低变化范围，画图更直观
    max_refer_count = math.sqrt(max_refer_count)
    min_refer_count = math.sqrt(min_refer_count)
    width_slope = (max_link_width - min_link_width) / (max_refer_count - min_refer_count)

    links=[]
    # links_item_format = """{source: '%s', target: '%s',
    #   lineStyle:{normal:{width: %f}}},
    #   """

    filtered_authors=set()
    for (refered_by,refered),count in relations:
        #跳过自引用，不然有可能画出孤立节点
        if refered_by==refered:
            continue
            # 小于门限跳过
        if count < count_to_plot_threshold:
            continue
        filtered_authors.add(refered_by)
        filtered_authors.add(refered)
        num=count
        count = math.sqrt(count)
        line_width = min_link_width + width_slope * (count - min_refer_count)
        links.append({'source':hant_2_hans(refered_by),'target':hant_2_hans(refered),'lineStyle':{'normal':{'width':line_width},'value':num,'tooltip':{'formatter':'{c}'}}})

    datanode=[]
    for author in filtered_authors:
        author_count = 0
        for (refered_by, refered), count in relations:
            if author == refered_by or author == refered:
                author_count += 1
        datanode.append({'name': hant_2_hans(author), 'value': author_count,'symbolSize':author_count*2.3})

    return links,datanode

@Tangnet.route('/Tangnetfun',methods=['GET'])
def Tangnetfunction():
    data={}
    relations_path='process/save/reference_relations.pkl'
    with open(relations_path, 'rb') as f:
        reference_relations_counter, reference_relations_text = pickle.load(f)

    relations, max_refer_count, min_refer_count = get_concerned_relations_by_range(reference_relations_counter, 100)
    fulltanglinks,fulltangdata=get_data_links_tang(relations, max_refer_count, min_refer_count)
    data['fulltang']=[fulltanglinks,fulltangdata]
    # data['fulltanglinks']=fulltanglinks
    # data['fulltangnodes']=fulltangdata
    # data['fulltangdata']=fulltangdata
    print(data['fulltang'][0])
    print(data['fulltang'][1])

    files_name_array=[('data/json_zh/early_tang_poets.txt','earlytang',1),('data/json_zh/high_tang_poets.txt','hightang',2),('data/json_zh/middle_tang_poets.txt','middletang',2),('data/json_zh/late_tang_poets.txt','latetang',1)]

    for authors_file_name,tangtype,threshold in files_name_array:
        with open(authors_file_name,'r',encoding='utf-8') as f:
            text=f.read()

        authors=set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter, authors)
        tanglinks,tangdata=get_data_links(relations, max_refer_count, min_refer_count)
        data[tangtype]=[tanglinks,tangdata]
        print(data[tangtype])

    data['categories']=[{"name":"早唐"},{"name":"盛唐"},{"name":"中唐"},{"name":"晚唐"},{"name":"其他"}]

    return jsonify(data)


@Tangnet.route('/Tangnetnetfun',methods=['GET'])
def Tangnetnetfun():
    data = {}
    netnum = int(request.args.get('value'))
    print(netnum)
    relations_path = 'process/save/reference_relations.pkl'
    with open(relations_path, 'rb') as f:
        reference_relations_counter, reference_relations_text = pickle.load(f)

    relations, max_refer_count, min_refer_count = get_concerned_relations_by_range(reference_relations_counter, netnum)
    fulltanglinks, fulltangdata = get_data_links_tang(relations, max_refer_count, min_refer_count)
    data['fulltang'] = [fulltanglinks, fulltangdata]
    # data['fulltanglinks']=fulltanglinks
    # data['fulltangnodes']=fulltangdata
    # data['fulltangdata']=fulltangdata
    print(data['fulltang'][0])
    print(data['fulltang'][1])
    files_name_array = [('data/json_zh/early_tang_poets.txt', 'earlytang', 1),
                        ('data/json_zh/high_tang_poets.txt', 'hightang', 2),
                        ('data/json_zh/middle_tang_poets.txt', 'middletang', 2),
                        ('data/json_zh/late_tang_poets.txt', 'latetang', 1)]

    for authors_file_name, tangtype, threshold in files_name_array:
        with open(authors_file_name, 'r', encoding='utf-8') as f:
            text = f.read()

        authors = set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter,
                                                                                         authors)
        tanglinks, tangdata = get_data_links(relations, max_refer_count, min_refer_count)
        data[tangtype] = [tanglinks, tangdata]
        print(data[tangtype])
    data['categories'] = [{"name": "早唐"}, {"name": "盛唐"}, {"name": "中唐"}, {"name": "晚唐"}, {"name": "其他"}]


    return jsonify(data)
