from os import preadv
from re import U
from datastructures.array2d import Array2D
import numpy as np
import sys
import string
import os
import time
from defaultWorld import StartingWorld
def main():
    def ansi(*args):
        PrintBuf=""
        for i in args:
            PrintBuf+="\033[" + i
        print(PrintBuf,sep="",end="")
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
        else:
            BeginSeq = StartingWorld
        ColDif= os.get_terminal_size().columns 
        ColDif-=len(BeginSeq[0])
        ColPad = [False for i in range((ColDif-8)//4)]  # 8 ensures we have space to prevent word wrap 
        RowDif= os.get_terminal_size().lines
        RowDif-= len(BeginSeq)+4
        for i in range(len(BeginSeq)):
            BeginSeq[i]= ColPad + BeginSeq[i]+ ColPad 
        ARowPad=[False for i in range(len(BeginSeq[0]))]
        TotalRowPad= [ARowPad for i in range (RowDif//2)]
        BeginSeq = TotalRowPad+ BeginSeq + TotalRowPad
        return (Array2D(starting_sequence=BeginSeq,data_type=bool))
    
    def screenInit():
        ansi(str(GameRows+1)+";1H")  
        ansi("3J", #clears scnreen
             "?1049h", #alt screen enable
             "?25l", #hides cursor
            (str(GameRows+2)+
             ''';1H n,m <Enter> -- Make n steps(-1=∞) waiting m seconds, quit to quit'''),# Guide text
            "7l", # disable line wrap - this one is even more iffy than others so dont really on it
            "0;0H",#puts cursor at begining of screen
             )
        for i in range(GameRows):# 
            ansi(*[ alive[int(World[i][v])] for v in range(GameCols)],"1E")
    # declared outside cause numpy
    #is a lil slow on creation
    # // these are reuseable
    def ArrStep():
        ansi("0;0H")
        nonlocal BufDown
        nonlocal BufUp
        BufSwap =None
        LocSum=0
        UpRow=World[0]
        #ansi(str(PrintStart)+";1H")
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
            UpRow = World[i]
            DownRow = World[i+1]
            LocSum=0
            lineprint=[]#space vs time thing here, could use Uprow to make this but more iteration
            for q in range(GameCols):
                LocSum+=int(DownRow[q])+int( (q<GameCols-1) and DownRow[q+1])
                BufUp[q]+= LocSum
                World[i][q] = bool((BufUp[q]==3) or (BufUp[q]==4 and UpRow[q]))
                lineprint.append(alive[int(World[i][q])])
                BufUp[q]=LocSum
                BufDown[q]+=LocSum
                LocSum=int(DownRow[q])
            ansi(*lineprint,"1E")
            BufSwap=BufUp
            BufUp=BufDown
            BufDown=BufSwap
        printbuf=[]
        for v in range(GameCols):
            World[GameRows-1][v]=bool((BufUp[v]==3) or (BufUp[v]==4 and World[GameRows-1][v]))
            printbuf.append(alive[int(World[GameRows-1][v])])
        ansi(*printbuf,"1E")
           ### Begin Print
    alive=["38;5;17m██", "38;5;224m██"]
    World = ArrInit()
    GameCols= (len(World[0]))
    GameRows= len(World)

    BufDown=np.empty(GameCols,int)
    BufUp=np.empty(GameCols,int) 
    screenInit()
    while 1>0:
        ansi((str(GameRows+3)+";1H"), "0m")
        YourWish=input("")
        ansi("1A","2K") # move cursor up and clear line
        if YourWish=="quit":
            ansi("0m")
            break
        else:
            YourWish = YourWish.split(",")
            if len(YourWish) == 2:
                n = int(YourWish[0] or 1)
                m = int(YourWish[1] or 1)
                i=0
                while i != n:
                    ArrStep()
                    time.sleep(m)
                    i+=1


if __name__ == '__main__':
        main()
