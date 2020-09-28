# Artificial Intelligence Assignment
#
# Week: 2
# Program Aim: To create a dictionary which maps word,tag to its frequency
# Date: September 28, 2020
# Author: Ritik Jain
# Team: Ritik Jain, Priyanshu Garg, Yugantar Arya
#
# Procedure:
#
# Phase 1: Construction of the dictionary in file
#
# Phase 2: Construction of the serialized dictionary for fast loading

import pickle
from os import mkdir
from os.path import isdir

def runWeek2():
    
    freqdict = dict()
    
    def buildDict(collect,dest):
        nonlocal freqdict
        fp = open(collect,"r")
        raw = fp.read().splitlines()
        fp.close()
        for item in raw:
            if item in freqdict: freqdict[item] += 1
            else: freqdict[item] = 1
        fp = open(dest,"w")
        for k,v in freqdict.items():
            fp.write(k+':'+str(v)+'\n')
        fp.close()

    def buildSerializedDict(dest):
        fp = open(dest,"wb")
        pickle.dump(freqdict,fp)
        fp.close()
    
    root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'
    print('Frequency Dictionary Construction Tool (Week 2) v1.0\n')
    print('Default Root: '+root)
    wish = input('Do you wish to continue with the default root? (y/N):')
    if wish.lower() == 'n':
        root = input('Enter the new root: ')
        print('Root set to: '+root)
        print('Continuing')
    else:
        print('Continuing with the default root')
    
    sroot = root+'filtered_data/'
    droot = root+'freq_dicts/'
    if not isdir(droot):
        mkdir(droot)

    print()
    print('Begin Phase 1: Dictionary Construction')
    print()
    print('Begin Constructing Test Dictionary')
    buildDict(sroot+'test-corpus.collect',droot+'test-dict.dict')
    testdict = freqdict.copy()
    print('End Constructing Test Dictionary')
    print()
    print()
    print('Begin Constructing Train Dictionary')
    buildDict(sroot+'train-corpus.collect',droot+'train-corpus.dict')
    traindict = freqdict.copy()
    print('End Constructing Train Dictionary')
    print()
    print()
    print('End Phase 1')
    print()

    print()
    print('Begin Phase 2: Serialized Dictionary Construction')
    print()
    print('Begin Constructing Serialized Test Dictionary')
    freqdict = testdict
    buildSerializedDict(droot+'test-dict.pickle')
    print('End Constructing Serialized Test Dictionary')
    print()
    print()
    print('Begin Constructing Serialized Train Dictionary')
    freqdict = traindict
    buildSerializedDict(droot+'train-corpus.pickle')
    print('End Constructing Serialized Test Dictionary')
    print()
    print('Dictionary Construction Sucessful!')

runWeek2()