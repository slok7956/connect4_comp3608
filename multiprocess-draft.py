import sys
from functools import reduce
from multiprocessing import Pool

#docs.python.org/2/library/threading.html#event-objects
import threading
from threading import Timer

#docs.python.org/3/library/timeit.html
import timeit
#print(timeit.timeit(stmt='print(str1[:5])',setup='str1 = "0"',number=1))
#time to print one digit per previous line: 6.591100827790797e-05
#therefore should be safe to try 0.9999 seconds for the interrupt

def num_in_a_row(state):
    way_keys = ["hori", "verti", "l_diag", "r_diag"]
    fin_keys = ["1", "2", "3", "4 or more"]
    checked_nodes = {k: [] for k in way_keys}
    red_dict = {k: 0 for k in fin_keys}
    yellow_dict = {k: 0 for k in fin_keys}
    winner = -1

    # index 0 is red, 1 is yellow
    fin_ls = [red_dict, yellow_dict]
    rows = [i for i in state.split(",")]
    i = 0
    while i < 6:    
        j = 0
        while j < 7:
            node = rows[i][j]
            if node != ".":
                # set index for color
                if node == "r":
                    index = 0
                if node == "y":
                    index = 1

                fin_ls[index]["1"] += 1

                # horizontal
                h = 1
                if (i,j) not in checked_nodes["hori"]:
                    while j+h < 7:
                        if rows[i][j+h] == node:
                            checked_nodes["hori"].append((i,j+h))
                            h += 1
                        else:
                            break
                
                # vertical
                v = 1
                if (i,j) not in checked_nodes["verti"]:
                    while i+v < 6:
                        if rows[i+v][j] == node:
                            checked_nodes["verti"].append((i+v,j))
                            v += 1
                        else:
                            break

                # left diagonal
                l = 1
                if (i,j) not in checked_nodes["l_diag"]:
                    while j-l >= 0 and i+l < 6:
                        if rows[i+l][j-l] == node:
                            checked_nodes["l_diag"].append((i+l,j-l))
                            l += 1
                        else:
                            break

                # right diagonal
                r = 1
                if (i,j) not in checked_nodes["r_diag"]:
                    while j+r < 7 and i+r < 6:
                        if rows[i+r][j+r] == node:
                            checked_nodes["r_diag"].append((i+r,j+r))
                            r += 1
                        else:
                            break                
                
                for ele in [h,v,l,r]:
                    if ele == 2:
                        fin_ls[index]["2"] += 1
                    if ele == 3:
                        fin_ls[index]["3"] += 1
                    if ele >= 4:
                        fin_ls[index]["4 or more"] += 1
                        winner = index
                
            j += 1
        i += 1
    return fin_ls,winner

def utility(winner):
    if winner == 0:
        return 10000
    if winner == 1:
        return -10000

def change_state(state, color, column):
    if color == "red":
        change = "r"
    if color == "yellow":
        change = "y"
    rows = [i for i in state.split(",")]
    i = 0
    j = column
    while i < 6 and j < 7:
        if rows[i][j] == ".":
            break
        else:
            i += 1
        if i == 6:
            j += 1
            i = 0
    rows[i] = rows[i][:j] + change + rows[i][j+1:]
    new_state = ",".join(rows)
    return new_state, j

def a_b_update(turn,score,alpha,beta):
  if turn=="red" and score>alpha:
    #print("Update alpha")
    alpha = score
  if turn=="yellow" and score<beta:
    #print("Update beta")
    beta = score
  #print(alpha,beta)
  return alpha,beta

def prune(turn,score,alpha,beta):
  p=False
  if turn=="red" and score>=beta:
    p=True
  if turn=="yellow" and score<=alpha:
    p=True
  #if beta <= alpha:
    #p=True
  #print(p)
  return p  

def evaluation(state):
    ls, winner = num_in_a_row(state)
    if winner != -1:
        return utility(winner)
    total = 0
    keys = ["1","2","3","4 or more"]
    for i in range(0,4):
        total += (ls[0][keys[i]] - ls[1][keys[i]])*(10**i)
    return total

def recurse(state, turn, score, alpha, beta, depth, max_depth=-1):
    
    if depth == 0:
        return score
    if (score == 10000 or score == -10000):
    #if (score == 10000 and turn == "yellow") or (score == -10000 and turn == "red"):
    #if (score == 10000 and turn == "red") or (score == -10000 and turn == "yellow"):
        return score
  
    alpha,beta=a_b_update(turn,score,alpha,beta)
    #fin_dict = {k:[] for k in range(0,7)}
    fin_dict = {}
    if turn == "red":
        next_turn = "yellow"
    if turn == "yellow":
        next_turn = "red"
    #update alpha & beta
    
    #expand next level of nodes
    i = 0
    while i < 7:
        #set child board state
        next_state, column = change_state(state, turn, i)
        #calculate score
        next_score=evaluation(next_state)
        #apply alpha/beta cutoff
        to_prune=prune(next_turn,next_score,alpha,beta)
        if to_prune:
          return score
          #break
          
        else:  
          #expand next node
          fin_dict.update({i:recurse(next_state, next_turn, next_score, alpha, beta, depth-1)})
        #advance column
        i = column
        i += 1

    if turn == "red":
        key = max(fin_dict, key=fin_dict.get)
    if turn == "yellow":
        key = min(fin_dict, key=fin_dict.get)
    if depth == max_depth:
        return key
    #if to_prune: 
        #return key
    return fin_dict[key]

def depth_search(contents, turn, max_depth):
    global next_move
    alpha=float('-inf')
    beta=float('inf')
    init_score=evaluation(contents)
    
    #first 6 possible boards
    first_move_state={}
    first_move_score={}
    for move in range(0,6):
      first_move_state[move]=(change_state(contents,turn,move)[0])
      first_move_score[move]=(evaluation(first_move_state[move]))

    init_data=[]
    #package data for recurse() as tuples
    for m in range(0,6):
      init_data.append((first_move_state[m],turn,first_move_score[m],alpha,beta,max_depth,max_depth))
    
    #multiprocessing
    vals=[]
    with Pool(processes=6) as pool:
      vals.append(pool.map(recurse,init_data))
    
    result = max(vals)
    next_move=f"{result}"
    return

def end_of_turn():
    global in_time
    in_time=False
    sys.exit()
    
next_move="0"
in_time=True
def connect_four(contents, turn):
    global next_move,in_time
    
    #send timeout signal
    #may be possible to add more 9s. haven't checked
    timeout=Timer(0.999999999999,end_of_turn)
    timeout.start()
    
    max_depth=2
    while in_time:
        depth_search(contents, turn, max_depth)
        max_depth += 1
    
    return next_move

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        board = '.ryyrry,.rryry.,..y.r..,..y....,.......,.......'
        player = 'red'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    print(connect_four(board, player))
