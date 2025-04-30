from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class IStack(Generic[T], ABC):
    ''' Interface for a stack data structure '''

    @abstractmethod
    def push(self, item: T) -> None:
        ''' Pushes an item onto the stack.
        
            Arguments:
                item: T -- The item to push onto the stack.
        '''
        ...

    @abstractmethod
    def pop(self) -> T:
        ''' Pops an item from the stack.
        
            Returns:
                T -- The item popped from the stack.
        '''
        ...

    @abstractmethod
    def peek(self) -> T:
        ''' Returns the top item on the stack without removing it.
        
            Returns:
                T -- The top item on the stack.
        '''
        ...

    @property
    @abstractmethod
    def empty(self) -> bool:
        ''' Returns True if the stack is empty, False otherwise. 
        
            Returns:
                bool: True if the stack is empty, False otherwise.
        '''
        ...

    @abstractmethod
    def clear(self) -> None:
        ''' Clears the stack. '''
        ...
    
    @abstractmethod
    def __contains__(self, item: T) -> bool:
        ''' Returns True if the item is in the stack, False otherwise.
        
            Arguments:
                item: T -- The item to search for.
                
            Returns:
                bool: True if the item is in the stack, False otherwise.
        '''
        ...
    
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ''' Returns True if the stack is equal to another stack, False otherwise.
        
            Arguments:
                other: object -- The other stack to compare.
                
            Returns:
                bool: True if the stack is equal to another stack, False otherwise.
        '''
        ...

    @abstractmethod
    def __len__(self) -> int:
        ''' Returns the number of items in the stack.
        
            Returns:
                int -- The number of items in the stack.
        '''
        ...

    @abstractmethod
    def __str__(self) -> str:
        ''' Returns a string representation of the stack.'''
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ''' Returns a string representation of the stack.'''
        ...