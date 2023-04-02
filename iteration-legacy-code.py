    #expand next level of nodes
    i = 0
    while i < 7:
        #set child board state
        next_state, column = change_state(state, turn, i)
        #i = column
        #calculate score
        next_score=evaluation(next_state)
        #alpha,beta=a_b_update(next_turn,next_score,alpha,beta)
        #check for pruning
        to_prune=prune(next_turn,next_score,alpha,beta)
        if to_prune:
            return score
        else:  
          #expand next node
          fin_dict.update({i:recurse(next_state, next_turn, next_score, alpha, beta, depth-1)})
        #advance column
        #i = column
        i += 1

        
        DICTIONARY THING
        next_level={}
    next_level.update({k:change_state(state,turn, for k in range(0,7)} 
