# datastructures.array.Array

""" This module defines an Array class that represents a one-dimensional array. 
    See the stipulations in iarray.py for more information on the methods and their expected behavior.
    Methods that are not implemented raise a NotImplementedError until they are implemented.
"""

from __future__ import annotations
from collections.abc import Sequence
import os
from typing import Any, Iterator, overload
import numpy as np
import gc
from numpy.typing import NDArray
from copy import Error, deepcopy
from datastructures.iarray import IArray, T

#some of this can just be done in numpy but since its a data structures class I will try to avoid using other ppls implemtations.

#Pop and delete and clear dont actually delte data, which is bad
#clears better cause @ least that will be garbage collected
#but pop and delete kind just ask nicely to not ask delted data
class Array(IArray[T]):  
    def __init__(self, starting_sequence: Sequence[T]=[], data_type: type=object) -> None:
        if type(data_type)==None or not isinstance(starting_sequence, Sequence):
            raise ValueError
        self.__data_type=data_type
        self.__item_count=len(starting_sequence)
        self.__space=2**(len(bin(self.__item_count))-2) or 1
        if not all(isinstance(i,data_type) for i in starting_sequence):
            raise TypeError
        self.__items = self.__copy_items(starting_sequence)
        ## -3 for leading 0b and to account for 2=2^1 rather than 2^0


    def __change_size(self, shrink = False) -> None:
        self.__item_count+=(1-(2*int(shrink)))
        if shrink and (self.__item_count*4 < (self.__space)):
            self.__space >>= 1
            self.__items=self.__copy_items(self.__items)
        if (not shrink) and (self.__item_count >= self.__space):
            self.__space <<=1
            self.__items=self.__copy_items(self.__items)
        gc.collect()# being overly safe

    def __copy_items (self,source) -> NDArray:
        temparr = np.empty(self.__space,dtype=self.__data_type) 
        for index in range(self.__item_count):
            temparr[index] = deepcopy(source[index])
        return (temparr)


    @overload
    def __getitem__(self, index: int) -> T:  ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:  ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        match index:
            case int():
                self.__check_index(index)
                if index < 0:
                    index = self.__item_count + index
                Item = self.__items[index]
                if isinstance(Item, np.generic):
                    return Item.item()
                else:
                    return Item      
            case slice():
                self.__check_index(index.stop)
                if index.start:
                    self.__check_index(index.start) 
                slicegen=self.__iterGen__(index)
                return Array(list(slicegen))
            case _:
                raise TypeError


    def __reversed__(self) -> Iterator[T]:
        revIter=self.__iterGen__(slice(self.__item_count-1,-1,-1))
        #hacky but should work unless theres a case where reverse is called but not intilized?
        return revIter 

    def __iter__(self):
        genobj=self.__iterGen__(slice(self.__item_count))
        return(genobj)
   
    def __iterGen__(self,slice):
        index = slice
        end = index.stop or (self.__item_count)
        curpos = index.start or 0 + (end<0)*(self.__item_count -1)
        step = index.step or (1-2*int(curpos >= end))
        assert step * (1-(2*int(curpos >= end))) > 0, \
        print("Steps invalid- increases distance to end:","curpos:step:end",curpos,step,end)
        end -= (end - curpos) % step
        while curpos != end:
            Item=self.__items[curpos]
            if isinstance(Item, np.generic):
                yield Item.item()
            else:
                yield Item 
            curpos += step



    def __setitem__(self, index: int, item: T) -> None: 
        #TODO convert to try expect
        if not isinstance(item,self.__data_type):
            raise TypeError("Arraytype",str(self.__data_type),"can't accept", str(type(item)))
        if abs(index) > self.__item_count- int(index > 0):
            raise IndexError
        self.__items[index] = item
        return

    def append(self, data: T) -> None:
        self.__check__item(data)
        self.__change_size(shrink=False)
        self.__items[self.__item_count-1]=data

    def append_front(self, data: T) -> None: 
        self.__change_size(shrink=False)
        for i, val in enumerate(self):
            self[i]=data
            data = val  
    


    def pop(self) -> T:
        # diffrent from delete, no loop overhead + return vaule
        popped = self[-1]
        self.__change_size(shrink=True)
        return(popped)
    
    def pop_front(self) -> None:
        popped=self[0]
        self.__delitem__(0) # calls change_size
        return popped
    
    def __len__(self) -> int: 
        return self.__item_count
    
    def __eq__(self, other: object) -> bool:
        #TODO swap to xor 
        if type(other) ==type(self) and len(other)==self.__item_count:
        ##shape checking before hand 
            return all(val == self[i] for i,val in enumerate(other))
        return False
    


    def __delitem__(self, index: int) -> None: # not done with pop cause that calls change size
        while index < len(self)-2:
            self[index] = self[index+1]
            index +=1
        self.pop()

    def __contains__(self, item: Any) -> bool:
        if not isinstance(item,self.__data_type): #shortcircuit diffrent types contain diffrent things 3.0 != 3
            return False
        return any(i==item for i in self)
    
    def clear(self) -> None:
        # could call change size but why?
        self.__space=0
        self.__item_count=0
        self.__items=np.empty(0, self.__data_type)
    
    def __check_index(self, index):
        if abs(index + int(index >= 0)) > len(self):
            raise IndexError 

    def __check__item(self,item): #these are both pretty small but were repeated alot of places.
       if not isinstance(item,self.__data_type):
            raise TypeError


    def __str__(self) -> str:
        return '[' + ', '.join(str(item) for item in self) + ']'
    
    def __repr__(self) -> str:
        return f'Array {self.__str__()}, Logical: {self.__item_count}, Physical: {len(self.__items)}, type: {self.__data_type}'
    

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
