import os
import random

def main():
    nCols= os.get_terminal_size().columns
    alive=["\033[48;5;33m  ", "\033[48;5;241m  "]
    for q in range(10):
        for i in range((nCols)//2):
            print(random.choice(alive),sep="",end="")
    print("\033[0m")


if __name__ == '__main__':
    main()
