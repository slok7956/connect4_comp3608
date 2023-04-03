from functools import reduce

# some_list = [[14], [215, 383, 87], [298], [374], [2,3,4,5,6,7]]
# single_list = reduce(lambda x,y: x+y, some_list)
# print(single_list)

# hori, verti, l_diag, r_diag
# count number of color, and track amount of in a row in a dict
# dict = {"amount":... ,"2": ..., "3": ..., "4 or more": ...}
# so only 1 iteration, reduce runtime, as the limit in tournament format is 1 second
# return a dictionary
# or a list with 2 dict, 1 is red, the other yellow
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

def evaluation(state):
    ls, winner = num_in_a_row(state)
    if winner != -1:
        return utility(winner)
    
    total = 0
    keys = ["1","2","3","4 or more"]
    for i in range(0,4):
        #subtract the number of yellow patterns from the red of the same size
        #weighted 1 per 1-token pattern; 10 per 2; 100 per 3; 1000 per 4 or more
        #negative for yellow advantage, positive for red
        total += (ls[0][keys[i]] - ls[1][keys[i]])*(10**i)
    return total

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
            return -1
    rows[i] = rows[i][:j] + change + rows[i][j+1:]
    new_state = ",".join(rows)
    #return new_state, j
    return new_state
  
#ALPHA-BETA UTILITY FUNCTIONS
def a_b_update(turn,score,alpha,beta):
  #print(turn,score,alpha,beta)
  
  if turn=="red" and score>alpha:
    alpha = score
    #print("Update alpha to ",alpha)
    
  if turn=="yellow" and score<beta:
    beta = score
    #print("Update beta to ",beta)
    
  #print(alpha,beta)
  #print(f"\n\n\n")
  return alpha,beta
    
def prune(turn,score,alpha,beta):
  p=False
  
  #if turn=="red" and score>=beta:
  if turn=="red" and alpha>=beta:
    p=True
  if turn=="yellow" and beta<=alpha:
    p=True
  #if beta <= alpha:
    #p=True
  
  #print(p)
  return p  

#MAIN CONTROL FLOW
def connect_four_ab(contents, turn, max_depth):
    #TEST CODE
    #print(f"{turn}'s turn, search depth: {max_depth}")
    alpha=float('-inf')
    beta=float('inf')
    init_score=evaluation(contents)
    
    recurse.counter = 0
    result = recurse(contents,turn,init_score,alpha,beta,max_depth,max_depth)
    
    return f"{result}\n{recurse.counter}"

def recurse(state, turn, score, alpha, beta, depth, max_depth=-1):
    #TEST CODE
    #print(f"Level {depth}: {turn}'s turn, score {score}, alpha {alpha}, beta {beta}")
    recurse.counter += 1
    if depth == 0:
        return score
    if (score == 10000 or score == -10000):
    #if (score == 10000 and turn == "yellow") or (score == -10000 and turn == "red"):
    #if (score == 10000 and turn == "red") or (score == -10000 and turn == "yellow"):
        return score
  
    #alpha,beta=a_b_update(turn,score,alpha,beta)
    fin_dict = {}
    if turn == "red":
        next_turn = "yellow"
    if turn == "yellow":
        next_turn = "red"
    #update alpha & beta
    alpha,beta=a_b_update(turn,score,alpha,beta)
    
    #calculate scores for next layer of nodes
    st={c:change_state(state, turn, c) for c in range(0,7)}
    for c in st.keys():
      if st[c] != -1:
        #set of keys only represents valid moves
        sc={c:evaluation(st[c])}
    
    a_b_vals={}
    for q in sc.keys():
      a_b_vals[q]=a_b_update(next_turn,sc[q],alpha,beta)
      alpha,beta=a_b_vals[q]
    
    #apply pruning cutoffs
    for n in sc.keys():
      if a_b_vals[n][1]<a_b_vals[n][0]:
        if turn=="red":
          #return alpha
          return a_b_vals[n][0]
        else:
          #return beta
          return a_b_vals[n][1]
      #expand next layer
      else:   
        fin_dict.update({n:recurse(st[n], next_turn, sc[n], a_b_vals[n][0], a_b_vals[n][1], depth-1)})
    
    #return score
    if turn == "red":
        key = max(fin_dict, key=fin_dict.get)
    if turn == "yellow":
        key = min(fin_dict, key=fin_dict.get)
    if depth == max_depth:
        return key
    return fin_dict[key]

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four_ab("..y.r..,..y.r..,..y.r..,.......,.......,.......", "red", 5))
    pass
