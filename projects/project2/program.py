from dataclasses import dataclass
import enum
from datastructures.bag import Bag
import random
import copy
def main():
    single_deck = []
    for i in range(14):
        for q in range(4):
            single_deck.append((i,q))
    print(single_deck)
    num_decks = random.randint(1,4)
    multideck = copy.deepycopy(single_deck)
    for _ in range(num_decks):
        multideck += multideck
    new_bag=Bag(*decklist)
if __name__ =='__main__':
        main()
