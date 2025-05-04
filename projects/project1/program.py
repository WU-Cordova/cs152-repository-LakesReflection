from os import preadv
from re import U
from datastructures.array2d import Array2D
import numpy as np
import sys
import string
import os
import time
def main():
    def ansi(Seq): 
        print("\033[",Seq,sep="",end="")
### take in data
    def ArrInit():
        BeginSeq=[]
        if len(sys.argv) > 1:
            f=open(sys.argv[1],"r")
            output=""
            TransDict=str.maketrans("Xx+-_|","111000",string.whitespace)
            for line in f:
                output= (line.translate(TransDict))
                BeginSeq.append(list(map(lambda x: bool(int(x)), [*output])))
        return (Array2D(starting_sequence=BeginSeq,data_type=bool))
    
    def screenInit():
        ansi("?1049l") #alt screen enable
        #ansi("?25l") #hides cursor

    # declared outside cause numpy
    #is a lil slow on creation
    # // these are reuseable
    def ArrStep():
        nonlocal BufDown
        nonlocal BufUp
        BufSwap =None
        LocSum=0
        UpRow=World[0]
        ansi(str(PrintStart)+";1H")
        for v in range(GameCols-1):
            LocSum+=int(UpRow[v])+int(UpRow[v+1])
            BufUp[v]=LocSum
            BufDown[v]=LocSum
            LocSum=int(UpRow[v])
        #looks strange to call twice but we actually mostly only work
        #with the second Row, So this isn't repeating the process
    #and primes the pump
    #could also stich bottom to top
        for i in range(GameRows-1):
            ansi("1E") #move cursor down a line
            UpRow = World[i]
            DownRow = World[i+1]
            LocSum=0
            for q in range(GameCols):
                LocSum+=int(DownRow[q])+int( (q<GameCols-1) and DownRow[q+1])
                BufUp[q]+= LocSum
                UpRow[q] = bool((BufUp[q]==3) or (BufUp[q]==4 and UpRow[q]))
                ansi(alive[int(UpRow[q])])
                BufUp[q]=LocSum
                BufDown[q]+=LocSum
                LocSum=int(DownRow[q])
            BufSwap=BufUp
            BufUp=BufDown
            BufDown=BufSwap
        ansi("0;49m")
        ansi("0m")
        for v in range(GameCols):
            World[GameRows-1][v]=bool((BufUp[v]==3) or (BufUp[v]==4 and World[GameRows-1][v]))
            ansi(alive[int(World[GameRows-1][v])])

    ### Begin Print
    alive=["0;34m██", "0;47m██"]
    World = ArrInit()
    GameCols= (len(World[0]))
    GameRows= len(World)
    PrintStart= (os.get_terminal_size().columns - GameCols)//2

    BufDown=np.empty(GameCols,int)
    BufUp=np.empty(GameCols,int)
    screenInit() 
    ArrStep()

if __name__ == '__main__':
    while 1>0:
        main()
        input()
