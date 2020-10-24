from pickle import load
from pickle import dump
from os import fstat

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
croot = root+'classifiers/v2/'
droot = croot+'distributions/'

print('Initializing... Please Wait')

#Defines Accuracy Metrics
class AccuracyMetrics:
    def __init__(self, metric = 'percent', equality = '0-error'):
        self.metric = metric
        self.equality = equality
        self.__evaldata__ = None
    def __equal__(self, v1, v2):
        if self.equality == '0-error':
            return v1 == v2
    def eval(self,value,predicted):
        if self.metric == 'percent':
            if self.__evaldata__ is None:
                self.__evaldata__ = (0,0)
            if self.__equal__(value,predicted):
                self.__evaldata__ = (self.__evaldata__[0]+1,self.__evaldata__[1]+1)
            else:
                self.__evaldata__ = (self.__evaldata__[0],self.__evaldata__[1]+1)
    def accuracy(self):
        if self.metric == 'percent':
            return self.__evaldata__[0]/self.__evaldata__[1]

#Loading test data, prediction table and backup prediction table
with open(droot+'utest.pickle','rb') as f:
    testdata = load(f)
with open(droot+'predtab.pickle','rb') as f:
    predtab = load(f)
    size_predtab = round(fstat(f.fileno()).st_size/10**6,2)
with open(droot+'backuppredtab.pickle','rb') as f:
    bpredtab = load(f)
    size_bpredtab = round(fstat(f.fileno()).st_size/10**6,2)
print('Evaluating the performance over the test data. Please wait')

#Evaluating accuracy over the test set
accmetrics = AccuracyMetrics()
accmetrics2 = AccuracyMetrics()
accmetrics3 = AccuracyMetrics()
a,b,c = 0,0,0
for sen in testdata:
    prev = None,None
    for word,tag in sen:
        key = (word,prev[0],prev[1])
        if key in predtab:
            ptag = predtab[key]
            accmetrics2.eval(tag,ptag)
            a += 1
        elif word in bpredtab:
            ptag = bpredtab[word]
            accmetrics3.eval(tag,ptag)
            b += 1
        else:
            ptag = None
            c += 1
        accmetrics.eval(tag,ptag)
        prev = word,ptag

#Printing the accuracy on test data
print(f'Accuracy over the Test Data: {round(accmetrics.accuracy()*100,2)}%')
print(f'Hits over prediction table: {round(a*100/(a+b+c),2)}%')
print(f'Accuracy over hits in prediction table: {round(accmetrics2.accuracy()*100,2)}%')
print(f'Hits over backup prediction table: {round(b*100/(a+b+c),2)}%')
print(f'Accuracy over hits in backup prediction table: {round(accmetrics3.accuracy()*100,2)}%')
print(f'Misses: {round(c*100/(a+b+c),2)}%')

#Saving stats
with open(croot+'stats.txt','w') as f:
    f.write(f'Classifier: v2\nSize: {size_predtab+size_bpredtab} MB\nAccuracy: {round(accmetrics.accuracy()*100,2)}%')