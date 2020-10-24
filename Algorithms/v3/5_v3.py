from pickle import load
from pickle import dump

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
droot = root+'classifiers/v3/distributions/'

# Load P(T|W) distribution
with open(droot+'T_WT.pickle',mode='rb') as file:
    t_wtd = load(file)

#Processing ambiguous tags
def put(d,k,v):
    if k in d:
        d[k] += v
    else:
        d[k] = v

t_wtd2 = dict()
for k,v in t_wtd.items():
    if '-' in k[1]:
        [a,b] = k[1].split('-')
        put(t_wtd2,(k[0],a,k[2]),v/2)
        put(t_wtd2,(k[0],b,k[2]),v/2)
    else:
        put(t_wtd2,k,v)
t_wtd = t_wtd2

# Approach: Assume the tag for a given word to be the most probable tag for that word
prd = dict()
for k,v in t_wtd.items():
    k2 = (k[0],k[2])
    if k2 in prd:
        if t_wtd[(k[0],prd[k2],k[2])] < v:
            prd[k2] = k[1]
    else:
        prd[k2] = k[1]

# Load Test data
with open(root+'filtered_data/test.pickle',mode='rb') as file:
    test_data = load(file)

# Restructure Test data to sentences:words
utest_data = []
for x1 in test_data:
    for x2 in x1:
        for x3 in x2:
            for x4 in x3:
                for x5 in x4:
                    sen = []
                    for x6 in x5:
                        if x6[0] != 'mw':
                            sen.append((x6[2],x6[1]))
                        else:
                            mw = ''
                            for x7 in x6[2]:
                                mw += x7[2]+' '
                            sen.append((mw[:-1],x6[1]))
                    utest_data.append(sen)

# Save predictions and restructured test data
with open(droot+'predtab.pickle',mode='wb') as file:
    dump(prd,file)
with open(droot+'utest.pickle',mode='wb') as file:
    dump(utest_data,file)
