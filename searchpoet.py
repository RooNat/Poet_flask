# -*-coding=utf-8-*-
'''
User:12433
Date:20220512
'''
from flask import Blueprint, render_template, request
from process.stconvert import  hant_2_hans
from process.stconvert import hans_2_hant
import sqlite3
import json
from flask import jsonify
from process.word_single import poetdata
searchpoet=Blueprint('searchpoet',__name__)


@searchpoet.route('/searchpoet')
def searchpage():  # put application's code here
    return render_template("search.html")

@searchpoet.route('/searchdata',methods=['GET'])
def searchdata():
    data={}
    wordcounter=[]
    conn = sqlite3.connect("data/cbdb_sqlite.db")
    c = conn.cursor()
    dname = str(request.args.get('name'))
    print(dname)
    if dname!='':
        t = hans_2_hant(dname)

    else:
        t=''
    sql = 'select c_female,c_death_age,c_birthyear,c_deathyear from BIOG_MAIN where c_name_chn=? and ((c_birthyear>=618 and c_birthyear<=907)\
or (c_deathyear>=618 and c_deathyear<=907) or (c_birthyear>=960 and c_birthyear<=1279) or (c_deathyear>=960 and c_deathyear<=1279))'
    cursor = c.execute(sql, (t,))
    conn.commit()
    result=[]
    for i in cursor:
        result.append(i)   #包含性别和死时的年龄
    if len(result)!=0:
        print(result[0])
        print("执行成功")
        data['name']=dname
        result[0]=list(result[0])
        if result[0][0]==0:
            data['female']="男"
        elif result[0][0]==1:
            data['female']="女"
        else:
            data['female']="不详"
        if result[0][1]==None:
            data['deathage']="不详"
        else:
            data['deathage']=result[0][1]
        poetword = {}
        if result[0][2]==None:
            result[0][2]=0
        if result[0][3]==None:
            result[0][3]=0
        if (result[0][2]>=618 and result[0][2]<=907) or (result[0][3]>=618 and result[0][3]<=907):
            data['chao']="唐朝"
            poetword=poetdata(dname,1)
            for i, j in poetword.items():
                wordcounter.append({"name": i, "value": j})
            data['wordcounter']=wordcounter
            with open('data/json_zh/authors.tang.json','r', encoding='utf-8') as f:
                obj=json.load(f)
                for i in obj:
                    if dname==i['name']:
                        data["intro"]=i['desc']
                        break
                    else:
                        data["intro"]='不详'
        elif (result[0][2]>=960 and result[0][2]<=1279) or (result[0][3]>=960 and result[0][3]<=1279):
            data['chao']="宋朝"
            poetword = poetdata(dname, 0)
            for i, j in poetword.items():
                wordcounter.append({"name": i, "value": j})
            data['wordcounter'] = wordcounter
            with open('data/json_zh/authors.songci.json','r', encoding='utf-8') as f:
                obj=json.load(f)
                for i in obj:
                    if dname==i['name']:
                        data["intro"]=i['desc']
                        break
                    else:
                        data["intro"]='不详'
        else:
            t1=open('data/json_zh/authors.tang.json','r', encoding='utf-8')
            s1=open('data/json_zh/authors.songci.json','r', encoding='utf-8')
            t2 = json.load(t1)
            s2 = json.load(s1)
            flag=0
            for h in t2:
                if dname==h['name']:
                    data['chao'] = "唐朝"
                    poetword = poetdata(dname, 1)
                    for i, j in poetword.items():
                        wordcounter.append({"name": i, "value": j})
                    data['wordcounter'] = wordcounter
                    data["intro"] = h['desc']
                    flag=1
                    break
            if flag==0:
                for h in s2:
                    if dname==h['name']:
                        data['chao'] = "宋朝"
                        poetword = poetdata(dname, 0)
                        for i, j in poetword.items():
                            wordcounter.append({"name": i, "value": j})
                        data['wordcounter'] = wordcounter
                        data["intro"] = h['desc']
                        flag=1
                        break
            if flag==0:
                data["intro"] = '不详'


        sql_loc = '''
            select distinct ADDRESSES.c_name_chn from BIOG_MAIN JOIN BIOG_ADDR_DATA on BIOG_MAIN.c_personid=BIOG_ADDR_DATA.c_personid 
            JOIN ADDRESSES on ADDRESSES.c_addr_id=BIOG_ADDR_DATA.c_addr_id 
            JOIN BIOG_ADDR_CODES on BIOG_ADDR_DATA.c_addr_type=BIOG_ADDR_CODES.c_addr_type where BIOG_MAIN.c_name_chn=? and BIOG_ADDR_CODES.c_addr_desc_chn='籍貫(基本地址)'
            '''

        cursor = c.execute(sql_loc, (t,))
        conn.commit()
        for i in cursor:
            re = i
        print(re)
        print(re[0])
        if re[0] == None:
            home = "不详"
            data['home'] = home  # 籍贯
        else:
            home = hant_2_hans(re[0])
            data['home'] = home  # 籍贯
        sql_location='''
        select ADDRESSES.x_coord,ADDRESSES.y_coord,ADDRESSES.c_name_chn,count(ADDRESSES.c_name_chn) 
        from BIOG_MAIN JOIN BIOG_ADDR_DATA on BIOG_MAIN.c_personid=BIOG_ADDR_DATA.c_personid 
        JOIN ADDRESSES on ADDRESSES.c_addr_id=BIOG_ADDR_DATA.c_addr_id JOIN BIOG_ADDR_CODES on BIOG_ADDR_DATA.c_addr_type=BIOG_ADDR_CODES.c_addr_type 
        where BIOG_MAIN.c_name_chn=? Group by ADDRESSES.c_name_chn
        '''
        cursor=c.execute(sql_location,(t,))
        conn.commit()
        data_loc=[]
        for i in cursor:
            if i[2]!='':
                data_loc.append({"name": hant_2_hans(i[2]), "value": [i[0], i[1], i[3]]})
        data['location']=data_loc
        print(data)
        c.close()
        conn.close()
    else:
        data['name']=dname
        data['female']='不详'
        data['deathage']='不详'
        data['home']='不详'
        data['location']=[{'name':'无','value':[]}]
        t1 = open('data/json_zh/authors.tang.json', 'r', encoding='utf-8')
        s1 = open('data/json_zh/authors.songci.json', 'r', encoding='utf-8')
        t2=json.load(t1)
        s2=json.load(s1)
        flag = 0
        for h in t2:
            if dname == h['name']:
                data['chao'] = "唐朝"
                poetword = poetdata(dname, 1)
                for i, j in poetword.items():
                    wordcounter.append({"name": i, "value": j})
                data['wordcounter'] = wordcounter
                data["intro"] = h['desc']
                flag = 1
                break
        if flag==0:
            for h in s2:
                if dname == h['name']:
                    data['chao'] = "宋朝"
                    poetword = poetdata(dname, 0)
                    for i, j in poetword.items():
                        wordcounter.append({"name": i, "value": j})
                    data['wordcounter'] = wordcounter
                    data["intro"] = h['desc']
                    flag = 1
                    break
        if flag == 0:
            data["intro"] = '不详'
    return jsonify(data)



