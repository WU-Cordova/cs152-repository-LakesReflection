from __future__ import annotations
from datastructures.array import Array
from datastructures.iarray import IArray T
import numpy as np
from collections.abc import Sequence
from typing import Any, Iterator, overload
from copy import deepcopy #something was shadowing my copy?
#Both Stack and 2d wanted to be able to set length (they both have work arounds) todo this
#but Ideologically I want to make both's size actually nonmutable
#(or at least implemnt sparse arrays for 2d )
class staticArray(Array(IArray[T])):
    def __init__(self, starting_sequence: Sequence[T]=[], data_type: type=object, length) -> None:
        if type(data_type)==None or not isinstance(starting_sequence, Sequence):
            raise ValueError
        self.__data_type=data_type
        self.__item_count=len(starting_sequence)
        self.__space=length
        self.__slice = slice(None)
        self.__items = np.zeros_like(self.__space,dtype=data_type)
        ## -3 for leading 0b and to account for 2=2^1 rather than 2^0
        for index in range(self.__item_count):
            if not isinstance(starting_sequence[index], self.__data_type):
                raise TypeError
            self[index] = deepcopy(starting_sequence[index])
    def change_size(self, shrink = False, amount=1) -> None:
        self.__item_count+=(1-(2*int(shrink)))*amount
  
    def copy_items (self) -> NDArray:
        pass
