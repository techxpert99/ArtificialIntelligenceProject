from pickle import load
from pickle import dump
from os import makedirs
from os.path import isdir

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/classifiers/v1_basic/'
with open(root+'train.pickle','rb') as f: wtd = load(f)


# Calculates the total sum of a distribution
# S = (sum over every random variable P(x1,...,xn))
def sumd(d):
    sumdst = 0
    for k,v in d.items():
        sumdst += v
    return sumdst

# Calculates the joint distribution i.e. P(W,T) from N(W,T) by normalization:
# P(W,T) = N(W,T) / (sum over w,t (N(W,T)) where w,t in W,T)
def normd(d):
    sumdst = sumd(d)
    jdst = dict()
    for k,v in d.items():
        jdst[k] = v/sumdst
    return jdst

# Marginalizes a probability distribution over a group of variables
# P(x1,...,xi-1,xi+1,...,xn) = sum over xi ( P(x1,...,xn)) )
def margd(d,m,bitmap = False):
    if not d.keys(): return
    else:
        if not bitmap:
            l = 0
            for k in d.keys():
                l = len(k)
                break
            incl = [True]*l
            if type(m) == int:
                incl[m] = False
            else:
                for i in m: incl[i] = False
        else:
            incl = m
            for i in range(len(incl)): incl[i] = not incl[i]
    mdst = dict()
    for k,v in d.items():
        k2 = []
        for i in range(len(k)):
            if incl[i]:
                k2.append(k[i])
        k2 = tuple(k2)
        if k2 in mdst:
            mdst[k2] += v
        else:
            mdst[k2] = v
    return mdst

# Conditions a probability distribution over a variable
# P(x1,...,xi-1,xi+1,...,xn | xi) = P(x1,...,xn)/margd(P(x1,...,xn),xi)
def cond(d,c,bitmap = False):
    if not d.keys(): return
    else:
        if not bitmap:
            l = 0
            for k in d.keys():
                l = len(k)
                break
            m = [True]*l
            cmap = [False]*l
            if type(c) == int:
                m[c] = False
                cmap[c] = True
            else:
                for i in c:
                    m[i] = False
                    cmap[i] = True         
        else:
            m = c
            for i in range(len(m)): m[i] = not m[i]
            cmap = c
    norm = margd(d,m,bitmap=True)
    con = dict()
    for k,v in d.items():
        k2 = []
        for i in range(len(cmap)):
            if cmap[i]: k2.append(k[i])
        k2 = tuple(k2)
        con[k] = v/norm[k2]
    return con


# The joint distribution P(W,T)
jd = normd(wtd)

# The tag distribution P(T)
td = margd(jd,0)

# Probability distribution P(W|T) = P(W,T) / P(T)
w_td = cond(jd,1)

# The word distribution P(W)
wd = margd(jd,1)

# Probability distribution P(T|W) = P(W,T) / P(W)
t_wd = cond(jd,0)

if not isdir(root+'distributions/'):
    makedirs(root+'distributions/')

# Saving P(W|T) distribution
with open(root+'distributions/W_T.pickle',mode='wb') as file:
    dump(w_td,file)

#Saving P(T|W) distribution
with open(root+'distributions/T_W.pickle',mode='wb') as file:
    dump(t_wd,file)