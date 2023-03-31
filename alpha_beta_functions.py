def a_b_reset(alpha,beta):
  alpha = float('-inf')
  beta = float('inf')
  
def a_b_update(turn,score,alpha,beta):
  
  if turn=="red" and score>alpha:
    alpha = score
  if turn=="yellow" and score<beta:
    beta = score
    
 def prune(turn,score,alpha,beta):
  p=False
  
  if turn=="red" and score>beta:
    p=True
  if turn=="yellow" and score<alpha:
    p=True
 
  return p
