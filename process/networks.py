# -*-coding=utf-8-*-
'''
User:12433
Date:20220509
'''

import os
import sys
import jieba
import thulac
import numpy as np
from snownlp import SnowNLP
from snownlp import sentiment

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from process.utiltool import ToolGeneral
from process.hyperpara import Hyperparams as hp

tool = ToolGeneral()
jieba.load_userdict(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dict', 'jieba_sentiment.txt'))
lex=thulac.thulac()

class SentimentAnalysis():
    """
    Sentiment Analysis with some dictionarys
    """

    def sentiment_score_list(self, dataset):
        seg_sentence = tool.sentence_split_regex(dataset)
        count1, count2 = [], []
        for sentence in seg_sentence:
            # words1=lex.cut(sentence)
            words = jieba.lcut(sentence, HMM=False)
            i = 0
            a = 0
            # words=[]  #在thulac下用
            # for w,g in words1:
            #     words.append(w)
            for word in words:
                """
                poscount 积极词的第一次分值;
                poscount2 积极反转后的分值;
                poscount3 积极词的最后分值（包括叹号的分值）      
                """
                idx=False
                idx1=False
                if word not in hp.posdict and word not in hp.negdict:
                    idx = any(f if f in word else False for f in hp.posdict)
                    idx1 = any(f if f in word else False for f in hp.negdict)
                poscount, negcount, poscount2, negcount2, poscount3, negcount3 = 0, 0, 0, 0, 0, 0  #
                if word in hp.posdict or idx==True:
                    if word in ['好', '真', '实在'] and words[min(i + 1, len(words) - 1)] in hp.pos_neg_dict and words[
                        min(i + 1, len(words) - 1)] != word:
                        continue
                    else:
                        if idx==True:
                            poscount += 1
                        else:
                            poscount+=1+0.5
                        c = 0
                        for w in words[a:i]:  # 扫描情感词前的程度词
                            id,id1,id2,id3,id4,id5,id6=False,False,False,False,False,False,False
                            if w not in hp.mostdict and w not in hp.verydict and w not in hp.moredict and w not in hp.ishdict and w not in hp.insufficientlydict and w not in hp.overdict and w not in hp.inversedict:
                               id= any(f if f in w else False for f in hp.mostdict)
                               id1 = any(f if f in w else False for f in hp.verydict)
                               id2 = any(f if f in w else False for f in hp.moredict)
                               id3 = any(f if f in w else False for f in hp.ishdict)
                               id4 = any(f if f in w else False for f in hp.insufficientlydict)
                               id5 = any(f if f in w else False for f in hp.overdict)
                               id6 = any(f if f in w else False for f in hp.inversedict)
                            if w in hp.mostdict or id==True:
                                poscount *= 4
                            elif w in hp.verydict or id1==True:
                                poscount *= 3
                            elif w in hp.moredict or id2==True:
                                poscount *= 2
                            elif w in hp.ishdict or id3==True:
                                poscount *= 0.5
                            elif w in hp.insufficientlydict or id4==True:
                                poscount *= -0.3
                            elif w in hp.overdict or id5==True:
                                poscount *= -0.5
                            elif w in hp.inversedict or id6==True:
                                c += 1
                            else:
                                poscount *= 1
                        if tool.is_odd(c) == 'odd':  # 扫描情感词前的否定词数
                            poscount *= -1.0
                            poscount2 += poscount
                            poscount = 0
                            poscount3 = poscount + poscount2 + poscount3
                            poscount2 = 0
                        else:
                            poscount3 = poscount + poscount2 + poscount3
                            poscount = 0
                        a = i + 1
                if word in hp.negdict or idx1==True:  # 消极情感的分析，与上面一致
                    if word in ['好', '真', '实在'] and words[min(i + 1, len(words) - 1)] in hp.pos_neg_dict and words[
                        min(i + 1, len(words) - 1)] != word:
                        continue
                    else:
                        if idx1==True:
                            negcount += 1
                        else:
                            # s=SnowNLP(word)
                            negcount += 1+0.5
                        d = 0
                        for w in words[a:i]:
                            id, id1, id2, id3, id4, id5, id6 = False,False,False,False,False,False,False
                            if w not in hp.mostdict and w not in hp.verydict and w not in hp.moredict and w not in hp.ishdict and w not in hp.insufficientlydict and w not in hp.overdict and w not in hp.inversedict:
                                id = any(f if f in w else False for f in hp.mostdict)
                                id1 = any(f if f in w else False for f in hp.verydict)
                                id2 = any(f if f in w else False for f in hp.moredict)
                                id3 = any(f if f in w else False for f in hp.ishdict)
                                id4 = any(f if f in w else False for f in hp.insufficientlydict)
                                id5 = any(f if f in w else False for f in hp.overdict)
                                id6 = any(f if f in w else False for f in hp.inversedict)
                            if w in hp.mostdict or id==True:
                                negcount *= 4
                            elif w in hp.verydict or id1==True:
                                negcount *= 3
                            elif w in hp.moredict or id2==True:
                                negcount *= 2
                            elif w in hp.ishdict or id3==True:
                                negcount *= 0.5
                            elif w in hp.insufficientlydict or id4==True:
                                negcount *= -0.3
                            elif w in hp.overdict or id5==True:
                                negcount *= -0.5
                            elif w in hp.inversedict or id6==True:
                                d += 1
                            else:
                                negcount *= 1
                    if tool.is_odd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1

                i += 1
                pos_count = poscount3
                neg_count = negcount3
                count1.append([pos_count, neg_count])
            if words[-1] in ['!', '！']:  # 扫描感叹号前的情感词，发现后权值*2
                count1 = [[j * 2 for j in c] for c in count1]

            for w_im in ['但是', '但','只是','却','却是','然而','可是','可']:
                if w_im in words:  # 扫描但是后面的情感词，发现后权值*5
                    ind = words.index(w_im)
                    count1_head = count1[:ind]
                    count1_tail = count1[ind:]
                    count1_tail_new = [[j * 5 for j in c] for c in count1_tail]
                    count1 = []
                    count1.extend(count1_head)
                    count1.extend(count1_tail_new)
                    break
            if words[-1] in ['?', '？']:  # 扫描是否有问好，发现后为负面
                count1 = [[0, 2]]

            count2.append(count1)
            count1 = []
        return count2

    def sentiment_score(self, s):
        senti_score_list = self.sentiment_score_list(s)
        if senti_score_list != []:
            negatives = []
            positives = []
            for review in senti_score_list:
                score_array = np.array(review)
                AvgPos = np.sum(score_array[:, 0])
                AvgNeg = np.sum(score_array[:, 1])
                negatives.append(AvgNeg)
                positives.append(AvgPos)
            pos_score = np.mean(positives)
            neg_score = np.mean(negatives)
            if pos_score >= 0 and neg_score <= 0:
                pos_score = pos_score
                neg_score = abs(neg_score)
            elif pos_score >= 0 and neg_score >= 0:
                pos_score = pos_score
                neg_score = neg_score
        else:
            pos_score, neg_score = 0, 0
        return pos_score, neg_score

    def normalization_score(self, sent):
        score1, score0 = self.sentiment_score(sent)
        if score1 > 4 and score0 > 4:
            if score1 >= score0:
                _score1 = 1
                _score0 = score0 / score1
            elif score1 < score0:
                _score0 = 1
                _score1 = score1 / score0
        else:
            if score1 >= 4:
                _score1 = 1
            elif score1 < 4:
                _score1 = score1 / 4
            if score0 >= 4:
                _score0 = 1
            elif score0 < 4:
                _score0 = score0 / 4
        return _score1, _score0


if __name__ == '__main__':
    sa = SentimentAnalysis()
    text = '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不尽，轻舟已过万重山。'
    et=jieba.lcut(text,HMM=False)
    print(sa.normalization_score(text))