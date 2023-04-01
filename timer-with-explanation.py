import sys
#docs.python.org/2/library/threading.html#event-objects
import threading
from threading import Timer
#docs.python.org/3/library/timeit.html
import timeit
#print(timeit.timeit(stmt='print(str1[:5])',setup='str1 = "0"',number=1))
#time to print one digit per previous line: 6.591100827790797e-05
#therefore should be safe to try 0.9999 seconds for the interrupt

next_move="0"

def end_of_turn():
    global next_move
    print(next_move)

def connect_four(contents, turn):
    global next_move
    
    #change time limit as needed
    timeout=Timer(0.9999,end_of_turn)
    timeout.start()
    
    return
