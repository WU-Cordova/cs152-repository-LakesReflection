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
from copy import deepcopy
from datastructures.iarray import IArray, T

#some of this can just be done in numpy but since its a data structures class I will try to avoid using other ppls implemtations.

#Pop and delete and clear dont actually delte data, which is bad
#clears better cause @ least that will be garbage collected
#but pop and delete kind just ask nicely to not ask delted data
class Array(IArray[T]):  

    def __init__(self, starting_sequence: Sequence[T]=[], data_type: type=object, length=None) -> None:
        if type(data_type)==None or not isinstance(starting_sequence, Sequence):
            raise ValueError
        self.__data_type=data_type
        self.__item_count=len(starting_sequence)
        self.__space=length or 2**((len(bin((self.__item_count )-bool(self.__item_count))))-2)
        self.__slice = slice(None)
        self.__items = np.empty(self.__space,dtype=data_type)
        ## -3 for leading 0b and to account for 2=2^1 rather than 2^0
        for index in range(self.__item_count):
            if not isinstance(starting_sequence[index], self.__data_type):
                raise TypeError
            self[index] = deepcopy(starting_sequence[index])

    def change_size(self, shrink = False, force=False) -> None:
        self.__item_count+=1-(2*int(shrink)) #
        if shrink and ((self.__item_count*4 < (self.__space))or force):
            self.__space = self.__space<<1
            self.__items=self.copy_items()
        elif (self.__item_count == self.__space) or force:
            self.__space = self.__space>>1
            self.__items=self.copy_items()
        gc.collect()# being overly safe

    def copy_items (self) -> NDArray:
        #bad way to do this need 2.5* size of array in memory but idk better way
        # also deep copy?
        temparr = np.empty(self.__space,dtype=self.__data_type)
        np.copyto(temparr,self.__items)
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
                    index = self.__item_count - index
                Item =self.__items[index]
                return Item.item() if isinstance(Item, np.generic) else Item
            case slice():
                self.__check_index(index.stop)
                if index.start:
                    self.__check_index(index.start) 
                self.__slice = index
                return Array(list(self))
            case _:
                raise TypeError

    def __check_index(self, index):
        if abs(index + int(index >= 0)) > len(self):
            raise IndexError 

    def __iter__(self):
        index = self.__slice
        self.__slice = slice(None)
        end = index.stop or (self.__item_count)
        curpos = index.start or 0 + (end<0)*(self.__item_count -1)
        step = index.step or (1-2*int(curpos >= end))
        assert step * (1-(2*int(curpos >= end))) > 0, print(curpos,step,end)
        end -= (end - curpos) % step
        print(curpos,step,end)
        while curpos != end:
            yield self.__items[curpos] 
            curpos += step

    def __setitem__(self, index: int, item: T) -> None: 
        #TODO convert to try expect
        if not isinstance(item,self.__data_type):
            raise TypeError
        if abs(index) > self.__item_count- int(index > 0):
            raise IndexError
        self.__items[index] = item
        return

    def append(self, data: T) -> None:
        self.change_size(shrink=False)
        self[-1]=data

    def append_front(self, data: T) -> None:
        self.change_size(shrink=False)
        for i, val in enumerate(self):
            self[i]=data
            data = val  
    


    def pop(self) -> T:
        # diffrent from delete, no loop overhead + return vaule
        popped = self[-1]
        # the self setter would throw type error
        self.change_size(shrink=True)
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
    

    def __reversed__(self) -> Iterator[T]:
        self.__slice = slice(-1,-1,0) 
        #hacky but should work unless theres a case where reverse is called but not intilized?
        return self

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
        # doesn't call __change_size__ cause its meant for incremental changes
        self.__space=0
        self.__item_count=0
        self.__items=np.empty(0, self.__data_type)
        self.__slice = slice(0)

    def __str__(self) -> str:
        return '[' + ', '.join(str(item) for item in self) + ']'
    
    def __repr__(self) -> str:
        return f'Array {self.__str__()}, Logical: {self.__item_count}, Physical: {len(self.__items)}, type: {self.__data_type}'
    

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
