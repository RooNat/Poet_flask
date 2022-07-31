# -*-coding=utf-8-*-
'''
User:12433
Date:20220509
'''
from sklearn.utils import shuffle
from process.networks import SentimentAnalysis
import json
SA = SentimentAnalysis()
import thulac

def predict(sent):
    """
    1: positif
    0: neutral
    -1: negatif
    """
    score1, score0 = SA.normalization_score(sent)
    if score1 == score0:
        result = 0
    elif score1 > score0:
        result = 1
    elif score1 < score0:
        result = -1
    return result


if __name__ == '__main__':
    all_data = []
    with open('../data/json_zh/data_sentiment_cut.txt', 'r', encoding='utf-8') as f:
        l=f.readlines()
        id=0
        for line in l:
            line=line.replace("\n","")
            print(line,id)
            id+=1
            pos,neg=SA.normalization_score(line)
            label=predict(line)
            all_data.append({"paragraphs":line,"label":label,"postive":pos,"negtive":neg})
            # all_data.append({"paragraphs": line, "label": label})
        f.close()
    # all_data = shuffle(all_data, random_state=1)
    # test_proportion = 0.05
    # test_idx = int(len(all_data) * test_proportion)
    # test_data = all_data[:test_idx]
    # train_data = all_data[test_idx:]
    # with open('data/json_zh/train_data.txt','w',encoding='utf-8') as d:
    #     for line in train_data:
    #         d.write(str(line)+'\n')
    #     d.close()
    # with open('data/json_zh/test_data.txt','w',encoding='utf-8') as t:
    #     for line in test_data:
    #         t.write(str(line) + '\n')
    #     t.close()
    with open("../data/json_zh/tangsong_label.json", 'w',encoding='utf-8') as h:
       h.write(json.dumps(all_data, ensure_ascii=False,indent=1))



            # test.append(line)
    # text = '向晚意不适，驱车登古原。夕阳无限好，只是近黄昏。'
