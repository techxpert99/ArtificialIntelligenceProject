from pickle import load
from pickle import dump

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
droot = root+'classifiers/v1_basic/distributions/'

# Load P(T|W) distribution
with open(droot+'T_W.pickle',mode='rb') as file:
    t_wd = load(file)

#Processing ambiguous tags
def put(d,k,v):
    if k in d:
        d[k] += v
    else:
        d[k] = v
t_wd2 = dict()
for k,v in t_wd.items():
    if '-' in k[1]:
        [a,b] = k[1].split('-')
        put(t_wd2,(k[0],a),v/2)
        put(t_wd2,(k[0],b),v/2)
    else:
        put(t_wd2,k,v)
t_wd = t_wd2

# Approach: Assume the tag for a given word to be the most probable tag for that word
prd = dict()
for k,v in t_wd.items():
    if k[0] in prd:
        if t_wd[(k[0],prd[k[0]])] < v:
            prd[k[0]] = k[1]
    else:
        prd[k[0]] = k[1]

# Load Test data
with open(root+'filtered_data/test.pickle',mode='rb') as file:
    test_data = load(file)

# Unstructure Test data
utest_data = []
for x1 in test_data:
    for x2 in x1:
        for x3 in x2:
            for x4 in x3:
                for x5 in x4:
                    for x6 in x5:
                        if x6[0] != 'mw':
                            utest_data.append((x6[2],x6[1]))
                        else:
                            mw = ''
                            for x7 in x6[2]:
                                mw += x7[2]+' '
                            utest_data.append((mw[:-1],x6[1]))

# Save predictions and unstructured test data
with open(droot+'predtab.pickle',mode='wb') as file:
    dump(prd,file)
with open(droot+'utest.pickle',mode='wb') as file:
    dump(utest_data,file)