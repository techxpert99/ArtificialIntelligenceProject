# Artificial Intelligence Assignment
#
# Week: 1
# Program Aim: To filter the text by extracting word and pos tag for the word
# Date: September 28, 2020
# Author: Ritik Jain
# Team: Ritik Jain, Priyanshu Garg, Yugantar Arya
#
# Procedure:
# The program does its job in 2 phases
# The number of phases could have been reduced to 1 ( and the time halved as well) but I went with this code
# since it doesn't take much time to preprocess all the files and it has to be done once; hence I prefered clarity
# of code over the small extra time it takes
#
# Phase 1 Filtration:
# The program processess all the raw xml files and converts them into filtered files
# The program makes use of the regex: {hw="([A-Za-z]+)"\\s+pos="([A-Za-z]+)"}, which is the heart of the program
# The above regex is a strict one (that it is case-sensitive). It could have been made more flexible,
# but given the consistency of the dataset, I went with the strict one.
# A filtered file contains all the word_tag combinations for its xml file
#
# Phase 2 Collection:
# The program then collects all the filtered files and assembles them into 1 big collect file
# The collect files for Test and Train dataset are made separately
#
# After the successful completion of both the phases, we obtain the processed data

from os import listdir
from re import findall
from os.path import isfile
from os.path import isdir
from os import mkdir
from sys import stdout

def runWeek1():

    def filterFile(source,dest,pat = 'hw="([A-Za-z]+)"\\s+pos="([A-Za-z]+)"',en="utf-8"):
        nonlocal stats
        fp = open(source,"r",encoding=en)
        lines = fp.readlines()
        text = str().join(lines)
        matches = findall(pat,text)
        fp.close()
        fp = open(dest,"w")
        for match in matches:
            fp.write(match[0]+'_'+match[1]+'\n')
        fp.close()
        stats += 1
        stdout.write(f'\rFiltered {stats} files')

    def filterRoot(sroot,droot):
        nonlocal stats
        if isfile(sroot):
            filterFile(sroot,droot+'.filtered')
        else:
            if not isdir(droot):
                mkdir(droot)
            for file in listdir(sroot):
                filterRoot(sroot+'/'+file,droot+'/'+file)

    def collect(root):
        nonlocal collector,stats
        if isfile(root):
            fp = open(root,"r")
            lines = fp.readlines()
            fp.close()
            for line in lines:
                collector.write(line)
            stats += 1
            stdout.write(f'\rCollected {stats} files')
        else:
            for file in listdir(root):
                collect(root+'/'+file)

    print('Text Filtration Tool (Week 1) v1.0\n')

    root = 'C:/Users/Ritik/Desktop/2021 Autumn Semester/Assignments/AI/'

    print('Default Root: '+root)
    wish = input('Do you wish to continue with the default root? (y/N):')
    if wish.lower() == 'n':
        root = input('Enter the new root: ')
        print('Root set to: '+root)
        print('Continuing')
    else:
        print('Continuing with the default root')
    print()
    print('Begin Phase 1: Filtration')
    stats = 0
    filterRoot(sroot=root+'raw_data',droot=root+'filtered_data')
    print()
    print('End Phase 1')
    print()

    print('Begin Phase 2: Collection')
    test = root+'filtered_data/Test-corpus'
    train = root+'filtered_data/Train-corpus'

    print('Begin Phase 2.1: Test Collection')
    collector = open(test+'.collect',"w")
    stats = 0
    collect(test)
    collector.close()
    print()
    print('End Phase 2.1')

    print('Begin Phase 2.2: Train Collection')
    collector = open(train+'.collect',"w")
    stats = 0
    collect(train)
    collector.close()
    print()
    print('End Phase 2.2')

    print('End Phase 2')
    print()
    print('Text filtration completed successfully!')