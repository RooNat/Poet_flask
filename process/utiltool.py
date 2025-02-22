# -*-coding=utf-8-*-
'''
User:12433
Date:20220509
'''

import re


class ToolGeneral():
    """
    Tool function
    """

    def is_odd(self, num):
        if num % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def load_dict(self, file):
        """
        Load dictionary
        """
        with  open(file, encoding='utf-8', errors='ignore') as fp:
            lines = fp.readlines()
            lines1=[]
            for l in lines:
                l=l.replace('\n','')
                lines1.append(l)
            lines = [l.strip() for l in lines1]
            print("Load data from file (%s) finished !" % file)
            dictionary = [word.strip() for word in lines]
        return set(dictionary)

    def sentence_split_regex(self, sentence):
        """
        Segmentation of sentence
        """
        if sentence is not None:
            sentence = re.sub(r"&ndash;+|&mdash;+", "-", sentence)
            sub_sentence = re.split(r"[。,，！!？?;；\s…~～]+|\.{2,}|&hellip;+|&nbsp+|_n|_t", sentence)
            sub_sentence = [s for s in sub_sentence if s != '']
            if sub_sentence != []:
                return sub_sentence
            else:
                return [sentence]
        return []

if __name__ == "__main__":
    #
    tool = ToolGeneral()
    #
    s = '我今天。昨天上午，还有现在'
    ls = tool.sentence_split_regex(s)
    print(ls)