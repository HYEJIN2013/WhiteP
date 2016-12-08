L1 = [1, 2, 3]
L2 = L1
print(L1)
>>[1, 2, 3]
print(L2)
>>[1, 2, 3]
L1 = [] # create new empty list, so L2 values still exist
print(L1)
>>[]
print(L2)
>>[1, 2, 3] # not cleared
L1 = L2
L1[:] = [] # substitute empty list to referenced list
print(L1)
>>[]
print(L2)
>>[]       # also cleared
