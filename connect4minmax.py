# need to complete evaluation, num_in_a_row, score unctions. then, implement minimax
# using the evaluation function

# import time

# start = time.time()

def connect_four_mm(contents, turn, max_depth):
    #TODO
    recurse.counter = 0
    result = recurse(contents,turn,max_depth,max_depth)
    return f"{result}\n{recurse.counter}"



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
 
    

def recurse(state, turn, depth, max_depth=-1):
    recurse.counter += 1
    print(recurse.counter)
    if depth == 0:
        return evaluation(state)   
    
    fin_dict = {k:[] for k in range(0,7)}
    if turn == "red":
        next_turn = "yellow"
    if turn == "yellow":
        next_turn = "red"
    i = 0
    while i < 7:
        next_state, column = change_state(state, turn, i)
        fin_dict[i].append(recurse(next_state, next_turn, depth-1))
        print(fin_dict)
        i = column
        i += 1
    # print(fin_dict)
    if turn == "red":
        key = max(fin_dict, key=fin_dict.get)
    if turn == "yellow":
        key = min(fin_dict, key=fin_dict.get)
    if depth == max_depth:
        return key
    return fin_dict[key]
    


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
    # if winner != -1:
    #     return utility(winner)

    total = 0
    keys = ["1","2","3","4 or more"]
    for i in range(0,4):
        total += (ls[0][keys[i]] - ls[1][keys[i]])*(10**i)
    return total


def utility(winner):
    if winner == 0:
        return 10000
    if winner == 1:
        return -10000
    

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four_mm("..y.r..,..y.r..,..y.r..,.......,.......,.......", "red", 2))