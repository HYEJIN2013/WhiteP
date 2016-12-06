def radixsort(arr):
	bins = []
	for i in range(0,10):                  #Creating empty bins
		bins.append([])
	a = 10                                 #To extract one's digit
	b = 1
	while True:
		result = []
		for elem in arr:
			digit = (elem % a) // b        #Extracting one's digit
			bins[digit].append(elem)       #Adding to bins
		if len(bins[0]) == len(arr):       #If entire array is sorted, then return
			return arr
		for i in range(0,10):              
			result.extend(bins[i])         #Dumping the bins in order to resultant array
			bins[i].clear()                #Clearing the bins for next digit
		arr = result
		print(arr)
		result = []
		a = a * 10                         #To extract next digit
		b = b * 10
	
arr = [5,213,55,21,2334,31,20,430]
radixsort(arr)
