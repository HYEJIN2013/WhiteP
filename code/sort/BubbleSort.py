n = int(input().strip())
a = list(map(int, input().strip().split(' ')))
count = 0

for i in range(len(a)):
    swapCount = 0
    for j in range(len(a)-1):
        if a[j] > a[j+1]:
            temp = a[j]
            a[j] = a[j+1]
            a[j+1] = temp
            swapCount += 1
    if swapCount == 0:
        break
    count += swapCount
    
print("Array is sorted in %d swaps." % count)
print("First Element: %d" % a[0])
print("Last Element: %d" % a[len(a)-1])
