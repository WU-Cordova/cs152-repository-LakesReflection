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
from numpy.typing import NDArray
from copy import deepcopy
from datastructures.iarray import IArray, T

#some of this can just be done in numpy but since its a data structures class I will try to avoid using other ppls implemtations.
class Array(IArray[T]):  

    def __init__(self, starting_sequence: Sequence[T]=[], data_type: type=object) -> None:
        if type(data_type)==None or not isinstance(starting_sequence, Sequence):
            raise ValueError
        self.__data_type=data_type
        self.__item_count=len(starting_sequence)
        self.__items = np.empty(
            2**((len(bin((self.__item_count )-bool(self.__item_count))))-2), 
            # -2 is to drop leading 0b, cast item count to bool to make 0 special case, elsewise subtracts 1 so minimun array size is achieved (which is also a power of two).
            dtype=data_type)
        ## -3 for leading 0b and to account for 2=2^1 rather than 2^0
        for index in range(self.__item_count):
            if not isinstance(starting_sequence[index], self.__data_type):
                raise TypeError
            self.__setitem__(index,deepcopy(starting_sequence[index]))
    @overload
    def __getitem__(self, index: int) -> T:  
        if abs(index) >= self.__item_count -1:
            raise IndexError
        Item =self.__items[index]
        return Item.item() if isinstance(Item, np.generic) else Item
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: # G
        cur = index.start or 0
        end = index.stop or (self.__item_count)-1
        step = index.step or 1
        items = []
        while (cur != end):
            items.append(self.__getitem__(cur))
            cur += step
        return items
    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        if not isinstance(index, (int, slice)):
            raise TypeError
        pass            

    def __setitem__(self, index: int, item: T) -> None: 
        if not isinstance(item, self.__data_type):
            raise TypeError
     #   if self.__item_count <= abs(index):
    #        raise IndexError    
        self.__items[index] = item
    def append(self, data: T) -> None:
        raise NotImplementedError('Append not implemented.')

    def append_front(self, data: T) -> None:
        raise NotImplementedError('Append front not implemented.')

    def pop(self) -> None:
        raise NotImplementedError('Pop not implemented.')
    
    def pop_front(self) -> None:
        raise NotImplementedError('Pop front not implemented.')

    def __len__(self) -> int: 
        return self.__item_count
    def __eq__(self, other: object) -> bool:
        ##shape checking before hand
        return(isinstance( other,type(self.__items)) and len(other)==len(self.__items) and bool (np.bitwise_xor(self.__items,other))) 
    def __iter__(self) -> Iterator[T]:
        self._curpos=self.__item_count
        return self
    def __next__(self):
        if self._curpos > 0:
            nxtVal = self.__getitem__(self._curpos)
            self._curpos -= 1
            return nxtVal
        raise StopIteration
    def __reversed__(self) -> Iterator[T]:
        raise NotImplementedError('Reversed not implemented.')

    def __delitem__(self, index: int) -> None:
        raise NotImplementedError('Delete not implemented.')

    def __contains__(self, item: Any) -> bool:
        if type(item) != self.__data_type: #shortcircuit diffrent types contain diffrent things 3.0 != 3
            return False
        for i in self:
            if i == item:
                return True
        return False
    
    def clear(self) -> None:
        self = self.__init__([],self.__data_type)

    def __str__(self) -> str:
        return '[' + ', '.join(str(item) for item in self) + ']'
    
    def __repr__(self) -> str:
        return f'Array {self.__str__()}, Logical: {self.__item_count}, Physical: {len(self.__items)}, type: {self.__data_type}'
    

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
