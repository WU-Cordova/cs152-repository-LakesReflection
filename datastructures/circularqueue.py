from typing import Any

from datastructures.array import Array
from datastructures.iqueue import IQueue, T
from copy import Error, deepcopy
import random
# <3 <- Totally the intials of Echo Oleary
#Todo
#EQ check
# dummy functions in parent class - east
#enque instiantiate
# REPR


class CircularQueue(IQueue[T]):
    def __init__(self, maxsize: int = 0, data_type=object) -> None:
        self.__max_size = maxsize        
        self.data_type = data_type 
        self.__bpt = 0
        self.__fpt=0
        self.__empty = True
        self.__carrnal = Array(starting_sequence=[0 for i in range(maxsize)],data_type=data_type)
    def enqueue(self, item: T) -> None:
        print(self.__repr__(),"grow")
        if not isinstance(item, self.data_type):
            raise TypeError
        self.__empty =False
        self.__carrnal[self.__bpt] = item
        self.__bpt =  (self.__bpt + 1) %(self.maxsize) 
    def dequeue(self) -> T:
        print(self.__repr__(),"shrink")
        if self.empty == True :
            raise BufferError
        prev = (self.__carrnal[self.__fpt])
        self.__fpt = (self.__fpt+1) %  (self.maxsize)
        if self.__fpt == self.__bpt:
            self.__empty=True
        return prev
               
    def clear(self) -> None:
        self.__fpt = 0
        self.__bpt = 0
    @property
    def front(self) -> T:
        if self.empty:
            raise IndexError
        return self.__carrnal[self.__fpt] #array should throw index array question mark?
    @property
    def full(self) -> bool:
        return ((self.__bpt == self.__fpt) and not self.__empty)
    @property
    def empty(self) -> bool:
        return self.__empty
        return dog
          # this relies on throwing an error for full
    @property
    def maxsize(self) -> int:
        return self.__max_size


    def __eq__(self, other: object) -> bool:
        if( (not isinstance(other, CircularQueue)) or# self.maxsize != other.maxsize or testing script doesnt like this but outline says max sizes should be eq
            self.data_type != other.data_type or
            len(self) != len(other) 
            ):
            return False
        bEqual= True
        for i in range(len(self)):
            elm = self.dequeue()
            bEqual = bEqual and (elm == other.front)
            self.enqueue(elm)
            other.enqueue(other.dequeue())
        return bEqual

    def __str__ (self) -> str:
        emplist =[]
        i= deepcopy(self.__fpt)
        # i want do while :(
        emplist.append(self.__carrnal[i])
        i = ((i+1) % (self.maxsize ))
        while (i != self.__bpt):
            emplist.append(self.__carrnal[i])
            i = ((i+1) % (self.maxsize ))
        return str(emplist)

    def __repr__ (self) -> str:
        return f'({self.__fpt}, {self.__bpt}), Q:{str(self)})'
    def __len__(self) -> int:
        if not self.full: # yes i could just keep a length var that would make my life easier
            return (self.__bpt - self.__fpt )%(self.maxsize)
        return self.maxsize
    # prove this but can get myself to inutvitely understand rn
    # if fpt < bpt, cause this array grows upwards then obvs the distance is just the diffrence
    # okay but what if bpt < fpt, i.e the pointers have looped?
    # remeber both of these are in mod maxsize
    # and taking the mod of neagtive number gives 
    # a conguernce class thats nessicarly positve and congruent to that neagtive distance

