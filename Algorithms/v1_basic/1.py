from os import listdir
from re import findall
from os.path import isfile
from os.path import isdir
from os import mkdir
from sys import stdout
import pickle
import xml.etree.ElementTree as ET

root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'

def wfilter(w):
    return ''.join(w.splitlines()).strip()

class Punctuation:
    def __init__(self,p):
        self.c5 = wfilter(p.get('c5'))
        self.punctuation = wfilter(p.text)
class Word:
    def __init__(self,w):
        self.word = wfilter(w.text)
        self.c5 = wfilter(w.get('c5'))
        self.pos = wfilter(w.get('pos'))
        self.hw = wfilter(w.get('hw'))
class MultiWord:
    def __init__(self,mw):
        self.elements = []
        self.c5 = wfilter(mw.get('c5'))
        for child in mw.getchildren():
            if child.tag == 'w':
                self.elements.append(Word(child))
            elif child.tag == 'c':
                self.elements.append(Punctuation(child))
class Sentence:
    def __init__(self,sentence):
        self.elements = []
        for child in sentence.getchildren():
            if child.tag == 'mw':
                self.elements.append(MultiWord(child))
            elif child.tag == 'w':
                self.elements.append(Word(child))
            elif child.tag == 'c':
                self.elements.append(Punctuation(child))
class Paragraph:
    def __init__(self,par):
        self.sentences = []
        for child in par.getchildren():
            if child.tag == 's':
                self.sentences.append(Sentence(child))
class Division:
    def __init__(self,div):
        self.paragraphs = []
        for child in div.getchildren():
            if child.tag == 'p':
                self.paragraphs.append(Paragraph(child))
class WText:
    def __init__(self,wtext):
        self.divisions = []
        for child in wtext.getchildren():
            if child.tag == 'div':
                self.divisions.append(Division(child))
class TextFile:
    def __init__(self,file):
        tree = ET.parse(file)
        root = tree.getroot()
        self.wtexts = []
        for child in root.getchildren():
            if child.tag == 'wtext':
                self.wtexts.append(WText(child))
class TrainData:
    def __init__(self):
        self.files = []
    def append(self,file):
        self.files.append(file)

def serializeTree(traindata):
    TRAINDATA = []
    for file in traindata.files:
        fil = []
        for wtext in file.wtexts:
            wtex = []
            for div in wtext.divisions:
                di = []
                for par in div.paragraphs:
                    pa = []
                    for sent in par.sentences:
                        sen = []
                        for element in sent.elements:
                            if type(element) == Word:
                                sen.append(('w',element.c5,element.word))
                            elif type(element) == Punctuation:
                                sen.append(('p',element.c5,element.punctuation))
                            elif type(element) == MultiWord:
                                mw = []
                                for mwelem in element.elements:
                                    if type(mwelem) == Word:
                                        mw.append(('w',mwelem.c5,mwelem.word))
                                    else:
                                        mw.append(('p',mwelem.c5,mwelem.punctuation))
                                sen.append(('mw',element.c5,mw))
                        pa.append(sen)
                    di.append(pa)
                wtex.append(di)
            fil.append(wtex)
        TRAINDATA.append(fil)
    return TRAINDATA

def buildTree(sroot):
    def filterFile(source):
        nonlocal traindata
        traindata.append(TextFile(source))

    def filterRoot(sroot):
        if isfile(sroot):
            filterFile(sroot)
        else:
            for file in listdir(sroot):
                filterRoot(sroot+'/'+file)

    traindata = TrainData()
    filterRoot(sroot)
    return traindata

if not isdir(root+'filtered_data'):
    mkdir(root+'filtered_data')

save_train = root+'filtered_data/train.pickle'
pickledtraindata = open(save_train,mode='wb')
pickle.dump(serializeTree(buildTree(root+'raw_data/train-corpus/')),pickledtraindata)
pickledtraindata.close()

save_test = root+'filtered_data/test.pickle'
pickledtestdata = open(save_test,mode='wb')
pickle.dump(serializeTree(buildTree(root+'raw_data/test-corpus/')),pickledtestdata)
pickledtestdata.close()