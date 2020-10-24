from pickle import load
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy

def runWeek3():
    root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
    with open(root+'freq_dicts/train-refdict.pickle','rb') as file:
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

    srtwordtab,srttagtab,srtwordtagtab = list(),list(),list()
    def sortTables(reverse=False):
        for word in worddict.keys():
            srtwordtab.append((worddict[word],word))
        for tag in tagdict.keys():
            srttagtab.append((tagdict[tag],tag))
        for wordtag in freq_dict.keys():
            srtwordtagtab.append((freq_dict[wordtag],wordtag))
        srtwordtab.sort(reverse=reverse)
        srttagtab.sort(reverse=reverse)
        srtwordtagtab.sort(reverse=reverse)
    
    sortTables(reverse=True)

    x1 = numpy.array([srtwordtab[i][1] for i in range(len(srtwordtab))])
    y1 = numpy.array([srtwordtab[i][0] for i in range(len(srtwordtab))])

    x2 = numpy.array([srttagtab[i][1] for i in range(len(srttagtab))])
    y2 = numpy.array([srttagtab[i][0] for i in range(len(srttagtab))])

    x3 = numpy.array([srtwordtagtab[i][1] for i in range(len(srtwordtagtab))])
    y3 = numpy.array([srtwordtagtab[i][0] for i in range(len(srtwordtagtab))])

    print('Most Frequent Words:')
    for u in x1[:10]: print(u)
    for v in y1[:10]: print(v)

    print('Most Frequent Tags:')
    for u in x2[:10]: print(u)
    for v in y2[:10]: print(v)

    print('Most Frequent Words:')
    for u in x3[:10]: print(u)
    for v in y3[:10]: print(v)

    plt.figure()
    ax = [plt.subplot2grid((2,3),(i,j)) for i in range(2) for j in range(3)]
    ax[0].scatter([_ for _ in range(len(x1))],y1,s=[10/(1+i) for i in range(len(x1))])
    ax[0].xlabel = 'Word'
    ax[0].ylabel = 'Frequency (in thousands)'
    ax[1].scatter([_ for _ in range(len(x2))],y2,s=[10/(1+i) for i in range(len(x2))])
    ax[1].xlabel = 'Tag'
    ax[1].ylabel = 'Frequency (in thousands)'
    ax[2].scatter([_ for _ in range(len(x3))],y3,s=[10/(1+i) for i in range(len(x3))])
    ax[2].xlabel = 'Word-Tag'
    ax[2].ylabel = 'Frequency (in thousands)'
    p1,p2,p3 = y1[:10],y2[:10],y3[:10]
    p1 = numpy.append(y1[:10],numpy.sum(y1[10:]))
    p2 = numpy.append(y2[:10],numpy.sum(y2[10:]))
    p3 = numpy.append(y3[:10],numpy.sum(y3[10:]))
    l1,l2,l3 = x1[:10],x2[:10],x3[:10]
    l1 = numpy.append(l1,'')
    l2 = numpy.append(l2,'')
    l3 = numpy.append(l3,'')
    ax[3].pie(p1)
    ax[4].pie(p2)
    ax[5].pie(p3)

    print(x2[-10:],y2[-10:])
    print(x1[-100:],y1[-100:])

    plt.show()
    
runWeek3()