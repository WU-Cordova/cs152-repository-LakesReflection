from __future__ import annotations

from ast import Raise
from dataclasses import dataclass
import os
from typing import Optional, Sequence
from datastructures.ilinkedlist import ILinkedList, T

# if you thought repeats were likely and the datatype was larger,
#you could save space by creating a singular holder for that data and then
# just having nodes refrence that, but evaultion costs hurts more common use cases
# so I'm not - <3
class LinkedList(ILinkedList[T]): 
    #Got rid of [T] cause no other data struc had it in that format and it threw error in pytest

    @dataclass
    class Node:
        data: T
        next: Optional[LinkedList.Node] = None
        previous: Optional[LinkedList.Node] = None
    def __init__(self, data_type: type = object) -> None:
        self.head = None
        self.tail =None
        self.__length = 0
        self.__data_type = data_type
        self.cur_node = self.head

     
    @staticmethod
    def from_sequence(sequence: Sequence[T], data_type: type=object) -> LinkedList[T]:
        ll = LinkedList(data_type)
        ll.head= ll.Node(None)
        ll.tail = ll.head
        for n in sequence:
            if not(isinstance(n,data_type)):
                raise TypeError
            ll.tail = ll.Node(n,previous=ll.tail)
            ll.tail.previous.next=ll.tail
            ll.__length +=1
        ll.head= ll.head.next
        return ll

    def IndexCheck(self):
        if self.__length == 0:
            raise IndexError
    
    def TypeCheck(self, item): #really I want these both to be macros not functions - <3
        if not isinstance(item, self.__data_type):
            raise TypeError ("Wrong type for thislist")
        return


    def append(self, item: T) -> None:
        self.TypeCheck(item)
        postfix_node = self.Node(item)
        if self.__length == 0:
            self.head = postfix_node
            self.tail = postfix_node
            self.__length += 1
        else:
            postfix_node.previous = self.tail
            self.tail.next = postfix_node
            self.tail = postfix_node
            self.__length += 1

    def prepend(self, item: T) -> None:
        self.TypeCheck(item)
        prefix_node = self.Node(item)
        if self.__length == 0:
            self.head = prefix_node
            self.tail = prefix_node
            self.__length += 1
        else:
            prefix_node.next = self.head
            self.head.previous = prefix_node
            self.__length += 1



    def link_insert (self,new_node) -> None:
        self.__length += 1
        if new_node.next:
            new_node.next.previous = new_node
        if new_node.previous:
            new_node.previous.next = new_node

    def link_drop (self, drop_node) -> None:
        self.__length -= 1
        if drop_node.previous:
            drop_node.previous.next = drop_node.next
        if drop_node.next:
            drop_node.next.previous = drop_node.previous

    #yes i could use my own iteration but I dont love the way thats implmented
    #and have concerns about messing with curnode in other functions
    # for i in linkedlist: insert_before(i,"cat")
    def insert_before(self, target: T, item: T) -> None:
        self.TypeCheck(item)
        self.TypeCheck(target)
        cur_node = self.head
        while cur_node.next != None:
            if target == cur_node.data:
                self.link_insert(self.Node(data=item, previous=cur_node.previous, next=cur_node))
                return
            cur_node = cur_node.next
        raise ValueError

    def insert_after(self, target: T, item: T) -> None:
        self.TypeCheck(item)
        self.TypeCheck(target)
        cur_node = self.tail
        while cur_node != None: # using length cause nodes could hold eqaul vaules but be dif objects
            if target == cur_node.data:
                self.link_insert(self.Node(data=item, previous=cur_node, next=cur_node.next))
                return
            cur_node = cur_node.previous
        raise ValueError


    def remove(self, item: T) -> None:
        self.TypeCheck(item)
        cur_node = self.head
        if cur_node == None:
            raise ValueError
        while cur_node.data != item:
            cur_node = cur_node.next
            if cur_node == None:
                raise ValueError
        self.link_drop(cur_node)

    def remove_all(self, item: T) -> None:
        self.TypeCheck(item)
        cur_node = self.head
        while cur_node != None:
            if cur_node.data == item:
                self.link_drop(cur_node)
            cur_node= cur_node.next
    
    def pop(self) -> T:
        self.IndexCheck()
        popped = self.tail
        self.tail = self.tail.previous
        self.__length -= 1
        if self.__length > 0:
            self.tail.next = None

        return popped.data
    # these two obvs do very similar things, so one might wanna genralize them to one func
    #not doing that cause it hurts readbilty
    def pop_front(self) -> T:
        self.IndexCheck()
        popped = self.head
        self.head = self.head.next
        self.__length -= 1
        if self.__length > 0: #i.e we didnt pop the only element
            self.head.previous = None
        return popped.data
   
    @property
    def front(self) -> T:
        self.IndexCheck()
        return self.head.data
    @property
    def back(self) -> T:
        self.IndexCheck()
        return self.tail.data
    
    @property
    def empty(self) -> bool:
        return self.__length ==0


    @property
    def count(self):
        return (self.__length)
    @property 
    def dtype(self):
        return self.__data_type


    def __len__(self) -> int:
        return self.__length

    def clear(self) -> None:
        self.tail = None
        self.head = None
        self.__length =0

    def __contains__(self, item: T) -> bool:
        bIn = False
        for i in self:
            bIn = (i == item) or bIn
        return bIn
    

    def __iter__(self) -> ILinkedList[T]:
        self.cur_node = self.head
        return self
    
    def __next__(self) -> T: 
        if self.cur_node == None:
            raise StopIteration
        hold = self.cur_node.data
        self.cur_node = self.cur_node.next
        return hold



    def __reversed__(self) -> ILinkedList[T]:
        cur_node = self.tail
        while cur_node.previous != None:
            yield cur_node.data
            cur_node = cur_node.previous
        return self

    def __eq__(self, other: object) -> bool:
        if ((not isinstance(other, LinkedList)) or
        (self.dtype != other.dtype) or 
        self.count != other.count ):
            return False
        bEq = False
        for i in zip(self, other):
            bEq = (i[0] == i[1]) or bEq
        return bEq
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
        return f"LinkedList({' <-> '.join(items)})"


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
