import numpy as np
cimport numpy as np

cimport cython
import random

from math import ceil
from libc.math cimport log2

@cython.wraparound(False)
@cython.boundscheck(False)
def PTCreate(double[::1] L):
  cdef int n = L.shape[0]
  cdef int m = ceil(log2(n))
  cdef double[:, :] PT = np.zeros([m+1,2**m])
  cdef int i, k
  
  with nogil:
      for i in xrange(n):
        PT[0,i] = L[i]
    
      for k in xrange(1,m+1):
        for i in xrange(2**(m-k)):
          PT[k,i] = PT[k-1,2*i] + PT[k-1,2*i+1]

  return PT

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef int PTSample(double[:, :] PT):
  cdef int m = PT.shape[0]
  cdef int i = 0
  cdef int k
  cdef double rn
 
  for k in xrange(m,0,-1):
      rn = random.random()
      i = 2*i + (PT[k,i]*rn < PT[k-1,2*i])
      #if PT[k,i]*rn < PT[k-1,2*i]:
      #    i = 2*i
      #else:
      #    i = 2*i +1
  return i

@cython.wraparound(False)
@cython.boundscheck(False)
def PTSample_many(double[:, :] PT, int N):
    cdef double[::1] out = np.empty(N)
    cdef int i
    
    for i in xrange(N):
        out[i] = PTSample(PT)
    return out

@cython.wraparound(False)
@cython.boundscheck(False)
def PTUpdate(double[:, :] PT, int ind, double newValue):
    cdef int k, m = PT.shape[0]
    PT[0,ind] = newValue

    with nogil:
        for k in xrange(1, m):
            ind = <int> (ind/2)
            PT[k,ind] = PT[k-1,2*ind] + PT[k-1,2*ind + 1]

    return PT

@cython.boundscheck(False)
def PTSample_many(double[:, :] PT, int N):
    cdef double[::1] out = np.empty(N)
    cdef int i
    
    for i in xrange(N):
        out[i] = PTSample(PT)
    return out

@cython.boundscheck(False)
def PTUpdate(double[:, :] PT, int ind, double newValue):
    cdef int k, m = PT.shape[0]
    PT[0,ind] = newValue

    with nogil:
        for k in xrange(1, m):
            ind = <int> (ind/2)
            PT[k,ind] = PT[k-1,2*ind] + PT[k-1,2*ind + 1]

    return PT
