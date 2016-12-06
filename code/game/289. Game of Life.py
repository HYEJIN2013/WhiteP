class Solution(object):
    def gameOfLife(self, board):
        """
        :type board: List[List[int]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        def Nnearby(i,j):
            n = 0
            if j >= 1 and board[i][j-1]==1: n+=1
            if j+1 < len(board[0]) and board[i][j+1]==1: n+=1
            if j >= 1 and i >= 1 and board[i-1][j-1]==1: n+=1
            if i >= 1 and j+1 < len(board[0]) and board[i-1][j+1]==1: n+=1
            if i+1 < len(board) and j >= 1 and board[i+1][j-1]==1: n+=1
            if i+1 < len(board)  and j+1 < len(board[0]) and board[i+1][j+1]==1: n+=1
            if i+1 < len(board) and board[i+1][j]==1: n+=1
            if i >= 1 and board[i-1][j]==1: n+=1
            return n
            
        l = []
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                if board[i][j] == 1:
                    if Nnearby(i,j) == 2 or Nnearby(i,j) == 3:
                        l.append([i,j])
                elif board[i][j] == 0:
                    if Nnearby(i,j) == 3:
                        l.append([i,j])
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                board[i][j] = 0
        for x in l:
            board[x[0]][x[1]] = 1
