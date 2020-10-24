from pickle import load
from pickle import dump
from os.path import isdir
from os import makedirs

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'

pickledtraindata = open(root+'filtered_data/train.pickle',mode='rb')
data = load(pickledtraindata)
pickledtraindata.close()

def put(val,dic):
    if val in dic:
        dic[val] += 1
    else:
        dic[val] = 1

droot = root+'classifiers/v1_basic/'
if not isdir(droot): makedirs(droot)

wtd = dict()
for x1 in data:
    for x2 in x1:
        for x3 in x2:
            for x4 in x3:
                for x5 in x4:
                    for x6 in x5:
                        if x6[0] != 'mw':
                            put((x6[2],x6[1]),wtd)
                        else:
                            w = ''
                            for x7 in x6[2]:
                                w += x7[2]+' '
                                put((x7[2],x7[1]),wtd)
                            wt = (w[:-1],x6[1])
                            put(wt,wtd)

pickledtraindict = open(droot+'train.pickle',mode='wb')
dump(wtd,pickledtraindict)
pickledtraindict.close()