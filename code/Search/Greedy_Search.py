import heapq
class PriorityQueue:
  def __init__(self, priorityFunction):
    self.priorityFunction = priorityFunction
    self.heap = []
      
  def push(self, item):
    heapq.heappush(self.heap, (self.priorityFunction(item), item))
      
  def pop(self):
    (_, item) = heapq.heappop(self.heap)
    return item
  
  def empty(self):
    return len(self.heap) == 0

def greedySearch(problem, heuristic):
  return graphSearch(problem, PriorityQueue(heuristic))
  
# problem is an instance of PacmanProblem
# food is the position of the food pellet (r,c)
def pacmanPathFinder(problem, food):
  manhattanDistanceHeuristic = lambda state: abs(state[0][0]-food[0]) + abs(state[0][1]-food[1])
  return greedySearch(problem, manhattanDistanceHeuristic)
