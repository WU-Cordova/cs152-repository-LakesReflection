import os

from datastructures.array import Array, T
from datastructures.istack import IStack

class ArrayStack(IStack[T]):
    ''' ArrayStack class that implements the IStack interface. The ArrayStack is a 
        fixed-size stack that uses an Array to store the items.'''
    def __init__(self, max_size: int = 0, data_type=object) -> None:
        self.max_size = max_size
        self.data_type= data_type
        self._top = 0
        self.__carrnal = Array(data_type=data_type)
        print("length of init array",len(self.__carrnal))
    def push(self, item: T) -> None:
        if not (isinstance(item,self.data_type)):
            raise ValueError
        if len(self.__carrnal) < self.max_size: 
            self.__carrnal.append(item)

    def pop(self) -> T:
        if not self.empty:
            return self.__carrnal.pop()
    
    def clear(self) -> None:
        self.__carrnal.clear()    
    @property
    def peek(self) -> T:
        return self.__carrnal[len(self.__carrnal)-1]
        
    @property
    def maxsize(self) -> int:
        return self.max_size
        ''' Returns the maximum size of the stack. 

            Examples:
                >>> s = ArrayStack(max_size=5, data_type=int)
                >>> s.maxsize
                5
        
            Returns:
                int: The maximum size of the stack.
        '''
        raise NotImplementedError    
    @property
    def full(self) -> bool:
        return len(self.__carrnal) == self.max_size
        ''' Returns True if the stack is full, False otherwise. 

            Examples:

        
            Returns:
                bool: True if the stack is full, False otherwise.
        '''

    @property
    def empty(self) -> bool:
        return bool(self.__carrnal)
    def __eq__(self, other: object) -> bool:
        if self.max_size != other.max_size:
            return False
        if self.__carrnal != other._carrnal: # this only works if both are echo stacks
            return False
        return True

    def __len__(self) -> int:
        return len(self.__carrnal)
    
    def __contains__(self, item: T) -> bool:
        return any(checked==item for checked in self.__carrnal)

    def __str__(self) -> str:
        ''' Returns a string representation of the stack.

            Examples:
                >>> s = ArrayStack(max_size=5, data_type=int)
                >>> s.push(1)
                >>> s.push(2)
                >>> s.push(3)
                >>> print(s)
                [1, 2, 3]
        
            Returns:
                str -- A string representation of the stack.
        '''
        return str([ i for i in self.__carrnal])
    
    def __repr__(self) -> str:
        ''' Returns a string representation of the stack.

            Examples:
                >>> s = ArrayStack(max_size=5, data_type=int)
                >>> s.push(1)
                >>> s.push(2)
                >>> s.push(3)
                >>> repr(s)
                'ArrayStack(5): items: [1, 2, 3]'
        
            Returns:
                str -- A string representation of the stack.
        '''
        return f"ArrayStack({self.max_size}): items: {str(self)}"
    
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')

