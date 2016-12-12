In [57]: a = arange(9).reshape(3,3)

In [58]: a
Out[58]:
array([[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]])

In [59]: b = 2 * a

In [60]: b
Out[60]:
array([[ 0,  2,  4],
       [ 6,  8, 10],
       [12, 14, 16]])


In [61]: hstack((a,b))
Out[61]:
array([[ 0,  1,  2,  0,  2,  4],
       [ 3,  4,  5,  6,  8, 10],
       [ 6,  7,  8, 12, 14, 16]])

In [62]: concatenate((a,b), axis=1)
Out[62]:
array([[ 0,  1,  2,  0,  2,  4],
       [ 3,  4,  5,  6,  8, 10],
       [ 6,  7,  8, 12, 14, 16]])
       
       
In [63]: vstack((a,b))
Out[63]:
array([[ 0,  1,  2],
       [ 3,  4,  5],
       [ 6,  7,  8],
       [ 0,  2,  4],
       [ 6,  8, 10],
       [12, 14, 16]])

In [64]: concatenate((a,b), axis=0)
Out[64]:
array([[ 0,  1,  2],
       [ 3,  4,  5],
       [ 6,  7,  8],
       [ 0,  2,  4],
       [ 6,  8, 10],
       [12, 14, 16]])



n [66]: dstack((a,b))
Out[66]:
array([[[ 0,  0],
        [ 1,  2],
        [ 2,  4]],

       [[ 3,  6],
        [ 4,  8],
        [ 5, 10]],

       [[ 6, 12],
        [ 7, 14],
        [ 8, 16]]])



In [69]: oned = arange(2)

In [70]: oned
Out[70]: array([0, 1])

In [71]: twice = 2 * oned

In [72]: twice
Out[72]: array([0, 2])

In [73]: column_stack((oned, twice))
Out[73]:
array([[0, 0],
       [1, 2]])
       
n [74]: row_stack((oned, twice))
Out[74]:
array([[0, 1],
       [0, 2]])
