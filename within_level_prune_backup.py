def recurse(state, turn, score, alpha, beta, depth, max_depth=-1):
    recurse.counter += 1
    #score = evaluation(state)
    #print("New node: ",turn,depth,score,alpha,beta)
    #alpha,beta=a_b_update(turn,score,alpha,beta)
    
    #if prune(turn,score,alpha,beta):
        #True
        #return score
    if depth == 0:
        return score
    if (score == 10000 and turn == "yellow") or (score == -10000 and turn == "red"):
        return score
    
    fin_dict = {k:[] for k in range(0,7)}
    if turn == "red":
        next_turn = "yellow"
    if turn == "yellow":
        next_turn = "red"
  
    i = 0
    while i < 7:
        #construct board state if next token played in column i
        next_state, column = change_state(state, turn, i)
        #calculate child node score
        next_score = evaluation(next_state)
        alpha,beta = a_b_update(next_turn,next_score,alpha,beta)
        #prune here
        if prune(next_turn,next_score,alpha,beta):
          break
        
        #explore unpruned branches
        fin_dict[i].append(recurse(next_state,next_turn,next_score,alpha,beta,depth-1))
        #try next column
        i = column
        i += 1

    print(fin_dict)
    if turn == "red":
        key = max(fin_dict, key=fin_dict.get)
    if turn == "yellow":
        key = min(fin_dict, key=fin_dict.get)
    if depth == max_depth:
        return key
    return fin_dict[key][0]
