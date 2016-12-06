from random import choice,randrange

def merge(left, right):
    result = []
    i ,j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(lst):
    if len(lst) <= 1:
        return lst
    middle = int( len(lst) / 2 )
    left = mergesort(lst[:middle])
    right = mergesort(lst[middle:])
    return merge(left, right)

def partition(lst,left,right):
    i = left+1
    pivot = lst[left]

    for j in range(left+1,right+1):
        if lst[j]<pivot:
            lst[j],lst[i] = lst[i],lst[j]
            i+=1
    pos = i-1
    lst[left],lst[pos] = lst[pos],lst[left]
    return pos

def quicksort(lst,left=False,right=False):
    if not left and not right:
        left = 0
        right = len(lst)-1
    if left<right:
        pivot_pos = partition(lst,left,right)
        quicksort(lst,left,pivot_pos-1)
        quicksort(lst,pivot_pos+1,right)
    return lst

if __name__ == '__main__':
   test_list = [7,7,8,10,12,18,9,1,4,6]
   print quicksort(test_list)
