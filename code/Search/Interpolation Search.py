interpolation_search(A[0...n-1], x):
  i = 0, j = n-1, lo = A[i], hi = A[j]

  if x < lo: 		
    return -1 	
  if x >= hi:
    i = j

  while i < j: 		
    k = i + ((j - i) * (x - lo)) / (hi - lo) 		
    mid = A[k] 		
    if x > mid:
      i = k + 1
      lo = mid
    elif x < mid:
      j = k - 1
      hi = mid
    else:
      return k
  return (x != A[i]) ? -1 : i
