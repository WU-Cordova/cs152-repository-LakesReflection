from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional, Sequence
from datastructures.ilinkedlist import ILinkedList, T

# if you thought repeats were likely and the datatype was larger,
#you could save space by creating a singular holder for that data and then
# just having nodes refrence that, but evaultion costs hurts more common use cases
# so I'm not - <3
class LinkedList(ILinkedList[T]): #Got rid of [T] cause no other data struc had it in that format and it threw error in pytest

    @dataclass
    class Node:
        data: T
        next: Optional[LinkedList.Node] = None
        previous: Optional[LinkedList.Node] = None

    def __init__(self, data_type: type = object) -> None:
        self.head = None
        self.tail = None
        self.__length = 0
        self.__data_type = data_type
     
    @staticmethod
    def from_sequence(sequence: Sequence[T], data_type: type=object) -> LinkedList[T]:
        raise NotImplementedError("LinkedList.from_sequence is not implemented")

    def append(self, item: T) -> None:
        postfix_node = self.Node(item)
        if self.__length == 0:
            self.head = postfix_node
            self.tail = postfix_node
            self.__length += 1
        else:
            postfix_node.previous = self.__tail
            self.tail.next = postfix_node
            self.__length += 1


    def prepend(self, item: T) -> None:
        prefix_node = self.Node(item)
        if self.__length == 0:
            self.head = prefix_node
            self.tail = prefix_node
            self.__length += 1
        else:
            prefix_node.next = self.head
            self.head.previous = prefix_node
            self.__length += 1

    def insert_before(self, target: T, item: T) -> None:
        raise NotImplementedError("LinkedList.insert_before is not implemented")

    def insert_after(self, target: T, item: T) -> None:
        raise NotImplementedError("LinkedList.insert_after is not implemented")

    def remove(self, item: T) -> None:
        raise NotImplementedError("LinkedList.remove is not implemented")

    def remove_all(self, item: T) -> None:
        raise NotImplementedError("LinkedList.remove_all is not implemented")

    def pop(self) -> T:
        popped = self.tail
        self.tail = self.tail.previous
        self.tail.next = None
        self.__length -= 1
        return popped.data
    # these two obvs do very similar things, so one might wanna genralize them to one func
    #not doing that cause it hurts readbilty
    def pop_front(self) -> T:
        popped = self.head
        self.head = self.head.next
        self.head.previous = None
        self.__length -= 1
        return popped.data
    @property
    def front(self) -> T:
        return self.head.data
    @property
    def back(self) -> T:
        return self.tail.data
    @property
    def empty(self) -> bool:
        return bool(self.__length)
    def __len__(self) -> int:
        return self.__length

    def clear(self) -> None:
        raise NotImplementedError("LinkedList.__contains__ is not implemented")
    def __contains__(self, item: T) -> bool:
        raise NotImplementedError("LinkedList.__contains__ is not implemented")

    def __iter__(self) -> ILinkedList[T]:
        raise NotImplementedError("LinkedList.__iter__ is not implemented")

    def __next__(self) -> T:
        raise NotImplementedError("LinkedList.__next__ is not implemented")
    
    def __reversed__(self) -> ILinkedList[T]:
        raise NotImplementedError("LinkedList.__reversed__ is not implemented")
    
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("LinkedList.__eq__ is not implemented")

    def __str__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return '[' + ', '.join(items) + ']'

    def __repr__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return f"LinkedList({' <-> '.join(items)}) Count: {self.count}"


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
