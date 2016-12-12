# -*- coding: utf-8 -*-
#make a tree of all the possible kmers in a given alphabet 

#this method creates a subtree given an alphabet and a parentnode 
def maketree(alphabet,parentnode):
  for letter in alphabet:
    parentnode.append([letter])
  return parentnode

print "======================TESTING METHOD: MAKETREE==================="
parent=['^']
parent=maketree('ACGT',parent)
print parent 

print "==============LEVEL 1 COMPLETE============="
#popout the last node-tree temporarily 
temproot=parent.pop()
temptree=maketree('ACGT',temproot)

print temptree

print '===================PLACE THE TEMPORARY TREE BACK================='
parent.insert(1,temptree)

print parent


def makelevel(parentlevel):
  for i in range(4):
    tempparent=parentlevel.pop()
    temptree=maketree('ACTG',tempparent)
    parentlevel.insert(1,temptree)
  return parentlevel

print '=========================TESTING makelevel METHOD============================='

newparent=['^']
print 'newparent'
print newparent
newparent=maketree('ACTG', newparent)
print 'maketree'
print newparent
someparent=makelevel(newparent)
print someparent

print 'POP SOMEPARENT'

for i in range(4):
  print someparent.pop()


#print '==============PARENT TEST============='
#parent1=['^']
#parent1=maketree('ACTG',parent1)
#print parent1
#print parent1.pop()
#for parentnode in parent1:
#  print parentnode
    



print '============================KMER TREE============================'
kmertree=['^']
kmertree=maketree('ACGT',kmertree)
#make the first level 
kmertree=makelevel(kmertree)
print kmertree
#make the second level 
