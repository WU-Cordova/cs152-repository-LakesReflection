import os
import random
import time

def main():
    def ansi(Seq): 
        #not args cause escape sequences
        #already confusing
        print("\033[",Seq,sep="",end="")
    nCols= os.get_terminal_size().columns
    nLines = os.get_terminal_size().lines
    printStart=(nLines-10)//2
    alive=["\033[0;25;34m██", "\033[0;25;43m██"]
    ansi("?1049l")
    ansi("3J") #clears screen
    ansi("?25l") #hides cursor
    numCells= nCols//2
    pad_left= bool(nCols % 2)
    for q in range(10):
        ansi(f"{printStart+q};H")
        #moves cursor to that row so it prints over top
        for i in range(numCells):
          #  print(random.choice(alive),sep="",end="")
            print((alive[(i+q) %2]),sep="",end="")
        if pad_left:
            ansi("0;30m█")
        ansi("30;40m")
    input()






if __name__ == '__main__':
    while 1>0:
        main()
        


