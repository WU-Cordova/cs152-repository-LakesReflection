import os
from datastructures.array import Array, T
from datastructures.istack import IStack
# this is a wildy inefficent implementation but 
# it does both manage to stay compatiable (proably with all i
# array implmentations and actually make the stack a fixed size
class ArrayStack(IStack[T]):
    ''' ArrayStack class that implements the IStack interface. The ArrayStack is a 
        fixed-size stack that uses an Array to store the items.'''

    def __init__(self, max_size: int = 0, data_type=object) -> None:
        self.max_size = max_size
        self.data_type=data_type
        self._MainfestedStack__top=0
        self._MainfestedStack__carrnal = Array([],data_type=data_type)
     
        ## these funcs do special thigns if no data has been pushed
    def push(self,item):
        if not isinstance(item,self.data_type):
                raise TypeError
        self._MainfestedStack__top += 1 
        for i in range(self.max_size):
            self._MainfestedStack__carrnal.append(item)
        print(vars(self))
        self.__class__ = MainfestedStack 

    def __str__(self) -> str:
        return str([])
    
    def __repr__(self) -> str:
        return f"ArrayStack({self.max_size}): items: {str(self)}"

    @property
    def maxsize(self) -> int:
        return self.max_size

    @property
    def full(self) -> bool:
        return False
    @property
    def empty(self) -> bool:
        return True

    def __len__(self) -> int:
        return 0
    def __contains__(self, item: T) -> bool:
        return False
    def __eq__(self, other: object) -> bool:
        return other.empty
    def clear(self) -> None:
        pass

    def peek(self):
        raise IndexError
    def pop(self):
        raise IndexError


class MainfestedStack(ArrayStack):
    def push(self, item: T) -> None:
        if not (isinstance(item,self.data_type)):
            raise ValueError
        if self.__top == self.max_size: 
            raise IndexError
        self.__carrnal[self.__top] = item
        ## keeping this as an array function
        #cause append acts more like stack than setting __top index to some vaule -EO

        # Actually I disagree with that but since the array is dynamic it has to use append
        #or u'd get an out of index error
        # and there is no good way to make a static array
        # that is compitable with Iarray
        # which expects a starting sequnce not a length
        # and also will accpet any object type
        # which means we cant safely assume zero casts to it


        #Even later echo
        #I solved this problem :)
        #with an intresting use of classes
        self.__top += 1


    def pop(self) -> T:
        if self.empty:
            raise IndexError
        self.__top -=1
        return self.__carrnal[self.__top]
    


    @property
    def peek(self) -> T: 
        return self.__carrnal[self.__top-1]
        
    def __eq__(self, other: object) -> bool:
        if ((not isinstance(other,ArrayStack)) or # this has to go first to ensure those attributes exist
            (self.max_size != other.max_size) or 
            (len(self) != len(other)) or 
            (self.data_type != other.data_type)):
                return False
        # this is not going to perform well,
        # but this is in python so that was always
        # going to be true, so just focusing on
        # making smthing that behaves like a stack
        copystack = ArrayStack(max_size= self.max_size, data_type=self.data_type)
        bEqual = True
        while len(self) > 0:
            other_elm = other.pop() 
            copystack.push(self.pop())
            if copystack.peek != other_elm:
                other.push(other_elm)
                self.push(copystack.pop()) 
                bEqual=False
                break 
        while len(copystack) > 0:
            copy_elm = copystack.pop()
            self.push(copy_elm)
            #other.push (copy_elm)
        other = self 
        return bEqual
        #this is prolly fine, but like kinda wacky cause 
        #comparing eqaulity has the possiblty of turning a deepcopy stack
        #back into a shallow copy
        # only need one copy of shared elements, cause they're shared
        # and most recent element already exists in a variable
        

    
    def __contains__(self, item: T) -> bool:
        copystack = ArrayStack(max_size= self.max_size, data_type=self.data_type)
        bFound = False
        while len(self) > 0:
            copystack.push(self.pop()) # verse declaring a var i think this saves a write each loop
            if copystack.peek == item: # but does call peek() idk how the function compares
                bFound = True             # rewritring a local var over and over
                break
        while len(copystack) > 0:  #need in both cases cause copystack is upside down
            self.push(copystack.pop())
        return bFound

    
    def __str__(self) -> str:
        return str([ self.__carrnal[i] for i in range(self.__top)])
    @property
    def full(self) -> bool:
        return self.__top == self.max_size

    @property
    def empty(self) -> bool:
        return not bool(self.__top)

    def __len__(self) -> int:
        return self.__top

    def clear(self) -> None:
        self.__top =0


    
if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')

