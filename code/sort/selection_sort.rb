#this is a an example of a sorting algorithm
def selection_sort(num_array)
  n = num_array.length
  j = 0
  while j < n - 1
    iMin = num_array[j]
    i = j+1
    while i < n
      if num_array[i] < iMin
        iMin = num_array[i]
      end
      puts num_array[i]
     i = i + 1
   end
   iMin_index = num_array.index(iMin)
   num_array[j], num_array[iMin_index] = num_array[iMin_index], num_array[j]
   j = j + 1
  end
  return num_array
end
