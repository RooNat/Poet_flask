# -*-coding=utf-8-*-
'''
User:12433
Date:20220510
'''

if __name__ == '__main__':
    fid=open('data_sentiment.txt', 'w', encoding='utf-8')
    with open('data_sentiment.txt','r',encoding='utf-8') as f:
        line=f.readlines()
        for h in line:
            if len(h)<170:
                fid.write(h)
        f.close()
    fid.close()

