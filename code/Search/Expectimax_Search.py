def value(problem, state):
  if problem.isTerminalState(state): return problem.getTerminalUtility(state)
  if state is a MAX node: return maxValue(problem, state)
  if state is a MIN node: return minValue(problem, state)
  if state is an EXP node: return expValue(problem, state)
  
def expValue(problem, state):
  v = 0
  for successor in problem.getSuccessors(state):
    v += problem.getProbability(state, successor) * value(problem, successor)
  return v
  
def maxValue(problem, state):
  v = -infinity
  for successor in problem.getSuccessors(state):
    v = max(v, value(problem, successor))
  return v
  
def minValue(problem, state):
  v = +infinity
  for successor in problem.getSuccessors(state):
    v = min(v, value(problem, successor))
  return v
