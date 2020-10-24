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

droot = root+'classifiers/v2/'
if not isdir(droot): makedirs(droot)

wtwtd = dict()
for x1 in data:
    for x2 in x1:
        for x3 in x2:
            for x4 in x3:
                for x5 in x4:
                    prv = None,None
                    for x6 in x5:
                        if x6[0] != 'mw':
                            put((x6[2],x6[1],prv[0],prv[1]),wtwtd)
                            prv = x6[2],x6[1]
                        else:
                            w = ''
                            for j in range(len(x6[2])):
                                x7 = x6[2][j]
                                if j != 0:
                                    w += x7[2]+' '
                                    put((x7[2],x7[1],prv[1],prv[0]),wtwtd)
                            wt = (w[:-1],x6[1])
                            put((wt[1],wt[0],prv[0],prv[1]),wtwtd)
                            prv = wt

pickledtraindict = open(droot+'train.pickle',mode='wb')
dump(wtwtd,pickledtraindict)
pickledtraindict.close()