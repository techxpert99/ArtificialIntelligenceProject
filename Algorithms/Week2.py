# Artificial Intelligence Assignment

# Week: 2
# Program Aim: To create a dictionary which maps word,tag to its frequency
# Date: September 28, 2020
# Author: Ritik Jain
# Team: Ritik Jain, Priyanshu Garg, Yugantar Arya

# Procedure:
# The application works in two phases. The first phase involves the construction
# of a human-readable dictionary files from both the collected test and train files.
# The second phase involves the construction of a serialized dictionary file
# for fast-access.

# Phase 1: Construction of the dictionary in file
# The collected files are used to create a dictionary (a hashmap) that
# maps a pair (word, tag) to frequency. The dictionary is stored in a human readable
# format in a dict file and as a hashmap in the memory.

# Phase 2: Construction of the serialized dictionary for fast loading
# This phase involves the serialization of the hashmap in memory using pickle, so that
# whenever the dictionary is required, it could be loaded rapidly in to the memory
# from disk.

import pickle
from os import mkdir
from os.path import isdir

def runWeek2():
    
    freqdict = dict()
    refineddict = dict()
    
    def buildDict(collect,dest):
        nonlocal freqdict
        fp = open(collect,"r",encoding='utf-8')
        raw = fp.read().splitlines()
        fp.close()
        for item in raw:
            if item in freqdict: freqdict[item] += 1
            else: freqdict[item] = 1
        fp = open(dest,"w",encoding='utf-8')
        for k,v in freqdict.items():
            fp.write(k+':'+str(v)+'\n')
        fp.close()

    def buildRefinedDict(dest):
        nonlocal refineddict
        for k,v in freqdict.items():
            c5,hw,pos,w = k.split('_')
            item = w+'_'+c5
            if item in refineddict:
                refineddict[item] += v
            else:
                refineddict[item] = v
        fp = open(dest,"w",encoding='utf-8')
        for k,v in refineddict.items():
            fp.write(k+':'+str(v)+'\n')

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
    
    sroot = root+'collected_data/'
    droot = root+'freq_dicts/'
    if not isdir(droot):
        mkdir(droot)

    print()
    print('Begin Phase 1: Dictionary Construction')
    print()
    print('Begin Constructing Test Dictionary')
    buildDict(sroot+'test-corpus.collect',droot+'test-dict.dict')
    testdict = freqdict.copy()
    buildRefinedDict(droot+'test-refdict.dict')
    testrefdict = refineddict.copy()
    print('End Constructing Test Dictionary')
    print()
    print()
    print('Begin Constructing Train Dictionary')
    freqdict = dict()
    refineddict = dict()
    buildDict(sroot+'train-corpus.collect',droot+'train-dict.dict')
    traindict = freqdict.copy()
    buildRefinedDict(droot+'train-refdict.dict')
    trainrefdict = refineddict.copy()
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
    freqdict = testrefdict
    buildSerializedDict(droot+'test-refdict.pickle')
    print('End Constructing Serialized Test Dictionary')
    print()
    print()
    print('Begin Constructing Serialized Train Dictionary')
    freqdict = traindict
    buildSerializedDict(droot+'train-dict.pickle')
    freqdict = trainrefdict
    buildSerializedDict(droot+'train-refdict.pickle')
    print('End Constructing Serialized Test Dictionary')
    print()
    print('Dictionary Construction Sucessful!')

runWeek2()