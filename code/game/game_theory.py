'''
Created on 2012-10-26
@author: xuhong
'''
import math
million = 1000000

def Q(state, action, U):
    ''' The expected value of taking an action in state, accordint to utility U'''
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        return U(state + 3*million) * 0.5 + U(state) * 0.5
    
def actions(state): return ['hold', 'gamble']
def identity(state): return state


U = identity

def best_action(state, actions, Q, U):
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)

print best_action(100, actions, Q, identity)
print best_action(100, actions, Q, math.log)
print best_action(2*million, actions, Q, math.log10)
print Q(1*million, 'gamble', math.log10)
print Q(1*million, 'hold', math.log10)
