from pickle import load
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy

def runWeek3():
    root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
    with open(root+'freq_dicts/train-dict.pickle','rb') as file:
        freq_dict = load(file)
    
    worddict,tagdict = dict(),dict()
    def buildTables():
        for key in freq_dict.keys():
            word,tag = key.split('_')
            if word in worddict:
                worddict[word] += freq_dict[key]
            else:
                worddict[word] = freq_dict[key]
            if tag in tagdict:
                tagdict[tag] += freq_dict[key]
            else:
                tagdict[tag] = freq_dict[key]
    
    buildTables()

    srtwordtab,srttagtab = list(),list()
    def sortTables(reverse=False):
        for word in worddict.keys():
            srtwordtab.append((worddict[word],word))
        for tag in tagdict.keys():
            srttagtab.append((tagdict[tag],tag))
        srtwordtab.sort(reverse=reverse)
        srttagtab.sort(reverse=reverse)
    
    sortTables(reverse=True)

    print(srtwordtab[:20])

    data = numpy.array([[i,srtwordtab[i][0]] for i in range(len(srtwordtab))])
    x = data[:,0]
    y = data[:,1]
    plt.scatter(x=x,y=y)
    plt.show()
runWeek3()