from os import listdir as ld
from os import makedirs as md
from os.path import isdir as d
from re import findall
from shutil import copyfile as cp

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/ArtificialIntelligenceProject/Algorithms/'

maxver = 0
for f in ld(root):
    if d(root+f) and f[0] == 'v':
        x = findall('v([0-9]*).*',f)
        maxver = max(maxver,int(x[0]))
        fmaxver = root+f+'/'

if not maxver:
    ver = 1
    md(root+f'v{ver}')
else:
    ver = maxver+1
    md(root+f'v{ver}')
    for f in ld(fmaxver):
        if f'v{maxver}' in f:
            d = f.replace(f'v{maxver}',f'v{ver}')
        else:
            d = f
        cp(fmaxver+f,root+f'v{ver}/'+d)