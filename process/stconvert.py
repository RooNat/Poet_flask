# -*-coding=utf-8-*-
'''
User:12433
Date:20220513
'''
import zhconv
def hant_2_hans(hant_str:str): #中文繁体转简体
    return zhconv.convert(hant_str,'zh-hans')

def hans_2_hant(hans_str:str):
    return zhconv.convert(hans_str, 'zh-hant') #简体转繁体