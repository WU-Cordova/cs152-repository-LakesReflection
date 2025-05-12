def ansi(*args):
    PrintBuf=""
    for i in args:
        PrintBuf+="\033[" + i
    print(PrintBuf,sep="",end="")
