import os
from datastructures.istack import IStack, T
from typing import Generic

from datastructures.linkedlist import LinkedList

class ListStack(Generic[T], IStack[T]):


    def __init__(self, data_type:object) -> None:
        self.__linkwork = LinkedList(data_type=data_type)

    @property
    def dtype (self):
        return self.__linkwork.dtype
    def push(self, item: T):
        self.__linkwork.append(item)
    def pop(self) -> T:
        if self.empty:
            raise IndexError
        return self.__linkwork.pop()
    def peek(self) -> T:
        if self.empty:
            raise IndexError
        return self.__linkwork.tail.data
    @property
    def empty(self) -> bool:
        return self.__linkwork.empty
    def clear(self):
       self.__linkwork.clear()
    def __contains__(self, item: T) -> bool:
        return item in self.__linkwork

    ## for explanation of what this is doing go look at array stack
    # could just check underlying array/ linkedlist but techincally that
    # touches others "Private" vars (the array/linked list itself), this gets aroudn that
    def __eq__(self, other) -> bool:
        if ((not isinstance(other,ListStack)) or # this has to go first to ensure those attributes exist
            (len(self) != len(other)) or 
            (self.dtype != other.dtype)):
                return False
        copystack = ListStack(data_type=self.dtype)
        bEqual = True
        while len(self) > 0:
            other_elm = other.pop() 
            copystack.push(self.pop())
            print(copystack, other_elm)
            if copystack.peek() != other_elm: # why is peek called here and not in array stack?
                other.push(other_elm)
                self.push(copystack.pop()) 
                bEqual=False
                break
            print (self, other, bEqual)
        while len(copystack) > 0:
            copy_elm = copystack.pop()
            self.push(copy_elm)
        other = self 
        return bEqual

    def __len__(self) -> int:
        return len(self.__linkwork)
    def __str__(self) -> str:
        return str(self.__linkwork)
    def __repr__(self) -> str:
        return self.__linkwork.__repr__()

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
