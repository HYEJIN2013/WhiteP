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
 
def astarGraphSearch(problem, heuristic):
  # A* uses path cost from start state + heuristic estimate to a goal
  totalCost = lambda state: len(state[1]) + heuristic(state)
  return graphSearch(problem, PriorityQueue(totalCost))
  
# problem is an instance of PacmanProblem
# food is the position of the food pellet (r,c)
def pacmanPathFinder(problem, food):
  manhattanDistanceHeuristic = lambda state: abs(state[0][0]-food[0]) + abs(state[0][1]-food[1])
  return astarGraphSearch(problem, manhattanDistanceHeuristic)
