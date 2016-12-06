test = [4,2,6,8,3,1,9,10,27,89,2]
from copy import deepcopy

def selection(lst):
    N = len(lst)

    for i in range(N):
        for j in range(i,N):
            if lst[j] < lst[i]:
                lst[i],lst[j] = lst[j],lst[i]
    return lst


def insertion(lst):
    for i in range(len(lst)):
        for j in range(i,0,-1):
            if lst[j] < lst[j-1]:
                lst[j],lst[j-1] = lst[j-1],lst[j]
            else:
                break
    return lst

def shellsort(lst):

    N = len(lst)
    h = 1
    
    while(h < N/3):
        h = 3*h+1

    while(h >= 1):
        for i in range(h,N):
            j = i
            while j >= h and lst[j] < lst[j-h]: 
                lst[j],lst[j-h] = lst[j-h],lst[j]
                j-=h
        h = h/3
    return lst
