from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class IQueue(Generic[T]):
    ''' Interface for a queue data structure '''

    @abstractmethod
    def enqueue(self, item: T) -> None:
        ''' Enqueues an item into the queue.
        
            Arguments:
                item: T -- The item to enqueue.
        '''
        ...

    @abstractmethod
    def dequeue(self) -> T:
        ''' Dequeues an item from the queue.
        
            Returns:
                T -- The item dequeued from the queue.
        '''
        ...

    @abstractmethod
    def front(self) -> T:
        ''' Returns the front item in the queue without removing it.
        
            Returns:
                T -- The front item in the queue.
        '''
        ...

    @abstractmethod
    def back(self) -> T:
        ''' Returns the back item in the queue without removing it.
        
            Returns:
                T -- The back item in the queue.
        '''
        ...

    @abstractmethod
    def __len__(self) -> int:
        ''' Returns the number of items in the queue.   
        
            Returns:
                int -- The number of items in the queue.
        '''
        ...

    @abstractmethod
    def empty(self) -> bool:
        ''' Returns True if the queue is empty, False otherwise. 
        
            Returns:
                bool: True if the queue is empty, False otherwise.
        '''
        ...

    @abstractmethod
    def clear(self) -> None:
        ''' Clears the queue. '''
        ...

    @abstractmethod
    def __contains__(self, item: T) -> bool:
        ''' Returns True if the item is in the queue, False otherwise.
        
            Arguments:
                item: T -- The item to search for.
                
            Returns:
                bool: True if the item is in the queue, False otherwise.
        '''
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ''' Compares two queues for equality.
        
            Arguments:
                other: object -- The other queue to compare.
                
            Returns:
                bool -- True if the queues are equal, False otherwise.
        '''
        ...

    @abstractmethod
    def __str__(self) -> str:
        ''' Returns a string representation of the queue.
        
            Returns:
                str -- A string representation of the queue.
        '''
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ''' Returns a string representation of the queue.
        
            Returns:
                str -- A string representation of the queue.
        '''
        ...
