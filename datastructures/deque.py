import os
from datastructures.iqueue import IQueue
from datastructures.linkedlist import LinkedList
from typing import TypeVar

T = TypeVar('T')

class Deque(IQueue[T]): # change var here too 
    """
    A double-ended queue (deque) implementation.
    """

    def __init__(self, data_type: type = object) -> None:
        self.__linkwork = LinkedList(data_type=data_type)
    @property
    def dtype (self):
        return self.__linkwork.dtype
    def enqueue(self, item: T) -> None:
        self.__linkwork.append(item) # link list throw error
    def dequeue(self) -> T:
        return self.__linkwork.pop_front()
    def enqueue_front(self, item: T) -> None:
        self.__linkwork.prepend(item)
    def dequeue_back(self) -> T:
        return self.__linkwork.pop()
    def front(self) -> T:
        if self.empty():
            raise IndexError
        return self.__linkwork.head.data
    def back(self) -> T:
        if self.empty():
            raise IndexError
        return self.__linkwork.tail.data
    def empty(self) -> bool:
        return self.__linkwork.empty
    def __len__(self) -> int:
        return len(self.__linkwork)
    def __contains__(self, item: T) -> bool:
        return item in self.__linkwork
    def __eq__(self, other) -> bool:
        if ((not isinstance(other,Deque)) or # this has to go first to ensure those attributes exist
            (len(self) != len(other)) or 
            (self.dtype != other.dtype)):
                return False
        bEqual= True
        for i in range(len(self)):
            elm = self.dequeue()
            bEqual = bEqual and (elm == other.front())
            self.enqueue(elm)
            other.enqueue(other.dequeue())
        return bEqual

    def clear(self):
        self.__linkwork.clear()
    def __str__(self) -> str:
        cur_node = self.__linkwork.head
        qlist =[]
        while cur_node:
            qlist.append(str(cur_node.data))
            cur_node = cur_node.next
        return("\n".join(qlist))
    def __repr__(self) -> str:
        return str(self)

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
