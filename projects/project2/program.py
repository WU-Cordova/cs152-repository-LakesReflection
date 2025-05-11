from dataclasses import dataclass
import enum
from datastructures.bag import Bag
import random

def main():
    decklist = []
    for i in range(14):
        for q in range(4):
            decklist.append((i,q))
    print(decklist)
    num_decks = random.randint(1,4)
    for _ in range(num_decks):
        decklist+=decklist
    new_bag=Bag(*decklist)
if __name__ =='__main__':
        main()
