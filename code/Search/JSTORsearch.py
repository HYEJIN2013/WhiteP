#!/usr/bin/python
import os, sys

metaPath = './PRE_1923_METADATA'


#Returns a list of all metafiles in './PRE_1923_METADATA'
def fileList(path):
    files = []
    for root, dirs, allFiles in os.walk(path):
        for allFile in allFiles:
            if allFile.endswith('.txt'):
                files =  files + [os.path.join(root, allFile)]
    return(files)

#Builds a Dictionary  of file: Title
def titleDict(files):
    dict = {}
    for file in files:  #opens each file
        f = open(file, 'r')
        lines = f.readlines()
        for line in lines:  # looks for title line
            if 'T1' == line[0:2]:
                title = line[5:].lower()
        dict[file] = title #set value of file to the title
        f.close
    return(dict)

#Builds a Dictionary  of file: Author
def authorDict(files):
    dict = {}
    for file in files:  #opens each file
        author = ''
        f = open(file, 'r')
        lines = f.readlines()
        for line in lines:  # looks for author lines
            if 'AU' == line[0:2]:
                author = author + line[5:].lower()
        dict[file] = author #set value of file to authors
        f.close
    return(dict)

#Searches through Dictionary  for the search term
def search(term, searchDict):
    result = []
    for i in searchDict:
        if term in searchDict[i]:
            result = result + [i, searchDict[i]]
    return result

def UI():
    sys.stdout.write('Script needs to be in the "R.I.P. Aaron Swartz - JSTOR archive 35GB" along side the subdirectory "PRE_1923_METADATA" and the 7z files in there extracted')
    sys.stdout.write(os.linesep)
    sys.stdout.write('Select search option:')
    sys.stdout.write(os.linesep)
    sys.stdout.write('  [1] Title')
    sys.stdout.write(os.linesep)
    sys.stdout.write('  [2] Author')
    sys.stdout.write(os.linesep)
    searchOption = input()
    
    if searchOption == '1' or searchOption == '2':  #check they entered an option
        
        sys.stdout.write('Enter keyword for search')
        sys.stdout.write(os.linesep)
        searchTerm = input().lower()
        
        if searchTerm != None:
            if searchOption == '1': #search titles
                return (search(searchTerm, titleDict(fileList(metaPath))))
            elif searchOption == '2': #search author
                return (search(searchTerm, authorDict(fileList(metaPath))))
    else:
        UI()


def displayResults(results):
    for i in results:
            print(i)

displayResults(UI())

raw_input()
