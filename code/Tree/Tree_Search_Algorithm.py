def treeSearch(problem, strategy):
  strategy.push(problem.getStartState())    
  while not strategy.empty():
    node = strategy.pop()
    if problem.isGoalState(node):
      return node[1]
    for move in problem.getSuccessors(node):            
      strategy.push(move)
  return None
