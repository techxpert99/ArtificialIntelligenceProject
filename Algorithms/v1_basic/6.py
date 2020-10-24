from pickle import load
from pickle import dump
from os import fstat

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
croot = root+'classifiers/v1_basic/'
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

#Loading test data and prediction table
with open(droot+'utest.pickle','rb') as f:
    testdata = load(f)
with open(droot+'predtab.pickle','rb') as f:
    size_predtab = round(fstat(f.fileno()).st_size/10**6,2)
    predtab = load(f)

print('Evaluating the performance over the test data. Please wait')

#Evaluating accuracy over the test set
accmetrics = AccuracyMetrics()
for word,tag in testdata:
    if word in predtab:
        ptag = predtab[word]
    else:
        ptag = ''
    accmetrics.eval(tag,ptag)

#Printing the accuracy on test data
print(f'Accuracy over the Test Data: {round(accmetrics.accuracy()*100,2)}%')

#Save stats
with open(croot+'stats.txt',mode='w') as file:
    file.write(f'Classifier: v1_basic\nSize: {size_predtab} MB\nAccuracy: {round(accmetrics.accuracy()*100,2)}%\n')