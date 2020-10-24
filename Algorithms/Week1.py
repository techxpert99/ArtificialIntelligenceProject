# Artificial Intelligence Assignment
#
# Week: 1
# Program Aim: To filter the text by extracting word and pos tag for the word
# Date: September 28, 2020
# Author: Ritik Jain
# Team: Ritik Jain, Priyanshu Garg, Yugantar Arya
#
# Procedure:
# The program does its job in 3 phases
# The number of phases could have been reduced to 1 but I went with this code
# since it doesn't take much time to preprocess all the files and it has to be done only once; hence I prefered clarity
# of code over the small extra time it takes
#
# Phase 1 Filtration:
# The program processess all the raw xml files and converts them into filtered files
# The program makes use of the regex:
# {<\\s*w[^>]*pos="([A-Za-z]*)"[^>]*>\\s*([^<\\s]*)\\s*<\\s*/w\\s*>}, which is the heart of the program
# The above regex is a flexible one. It could have been made stricter, given the consistency of the dataset,
# but I still went with the flexible version since it is more general.
# A filtered file contains all the word_tag combinations for its xml file.
# The word,tag combinations are stored in a case sensitive manner.
#
# Phase 2 Collection:
# The program then collects all the filtered files and assembles them into 1 big collect file
# The collect files for Test and Train dataset are made separately
#
# Phase 3 Verification:
# The verification phase verifies that the filtered data matches the raw data.
# This is accomplished by rescanning the raw data with a simpler regex {<\\s*/\\s*w\\s*>} (only for </w> tags)
# and maintaing the total count of word,tag combinations for each file.
# The filtered files are also rescanned, but the regex used is {;}
# After the scan is complete, the verification ratio and the accuracy are displayed.
# If the accuracy > 95 %, the verification could be assumed to be successful.
# 
# After the successful completion of all the phases, we obtain the processed data

from os import listdir
from re import findall
from os.path import isfile
from os.path import isdir
from os import mkdir
from sys import stdout

def runWeek1(): 

    def filterFile(source,dest,pat = '<\\s*w[^>]*c5\\s*=\\s*"([^"]*)"[^>]*hw\\s*=\\s*"([^"]*)"[^>]*pos\\s*=\\s*"([^"]*)"[^>]*>\\s*([^<\\s]*)\\s*<\\s*/w\\s*>',en="utf-8"):
        nonlocal stats
        fp = open(source,"r",encoding=en)
        text = str().join(fp.read().splitlines())
        matches = findall(pat,text)
        fp.close()
        fp = open(dest,"w",encoding=en)
        for match in matches:
            fp.write(match[0]+'_'+match[1]+'_'+match[2]+'_'+match[3]+'\n')
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

    def collect(root,en="utf-8"):
        nonlocal collector,stats
        if isfile(root):
            fp = open(root,"r",encoding=en)
            text = fp.read()
            fp.close()
            collector.write(text)
            stats += 1
            stdout.write(f'\rCollected {stats} files')
        else:
            for file in listdir(root):
                collect(root+'/'+file)

    def verify(root):
        def count(file,en,pat,out,delim=True):
            with open(file,'r',encoding=en) as f:
                if delim:
                    L = len(findall(pat,str().join(f.read().splitlines())))
                else:
                    L = len(findall(pat,f.read()))
                out.write(f'{file}${L}\n')
                return L
            return 0
        def explore(root,en,pat,out,delim=True):
            if isfile(root):
                return count(root,en,pat,out,delim)
            else:
                total = 0
                for file in listdir(root):
                    total += explore(root+'\\'+file,en,pat,out,delim)
                return total
        
        if(not isdir(root+'verification_records')):
            mkdir(root+'verification_records')
        
        with open(root+'verification_records/raw.verify','w') as out:
            xcount1 = explore(root+'raw_data','utf-8','<\\s*/\\s*w\\s*>',out)
            out.write(f'$TOTAL$ = {xcount1}')

        with open(root+'verification_records/filtered.verify','w') as out:
            xcount2 = explore(root+'filtered_data','utf-8','\n',out,False)
            out.write(f'$TOTAL$ = {xcount2}')

        ratio = xcount2/xcount1
        acc = abs((1-abs(ratio-1)))*100
        print(f'Verification Ratio: {round(ratio,4)}')

        print(f'Estimated Accuracy: {round(acc,2)}%')

        with open(root+'verification_records/statistics.txt','w') as out:
            out.write(f'Estimated Raw Tags:{xcount1}\nProcessed Raw Tags:{xcount2}\nVerification Ratio:{ratio}\nAccuracy:{acc}\n')
        return ratio

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
    if not isdir(root+'collected_data'):
        mkdir(root+'collected_data')
    collector = open(root+'collected_data/Test-corpus.collect',"w",encoding="utf-8")
    stats = 0
    collect(test)
    collector.close()
    print()
    print('End Phase 2.1')

    print('Begin Phase 2.2: Train Collection')
    collector = open(root+'collected_data/Train-corpus.collect',"w",encoding="utf-8")
    stats = 0
    collect(train)
    collector.close()
    print()
    print('End Phase 2.2')

    print('End Phase 2')
    print()
    print('Begin Phase 3: Verification')
    verify(root)
    print('End Phase 3')
    print()
    print('Text filtration completed successfully!')
