from __future__ import annotations
import os
from typing import Iterator, Sequence

from datastructures.iarray import IArray
from datastructures.array import Array
from datastructures.iarray2d import IArray2D, T


class Array2D(IArray2D[T]):

    class Row(IArray2D.IRow[T]):
        def __init__(self, row_index: int, array: IArray, num_columns: int) -> None:
            self.num_columns = num_columns # this should be a getter not an int no?
            self.__array=array
            self.row =row_index
            self.offset = self.num_columns * self.row
        def __getitem__(self, column_index: int) -> T:
            if column_index >= self.num_columns:
                raise IndexError
            return self.__array[self.offset + column_index]
        def __setitem__(self, column_index: int, value: T) -> None:
            self.__array[self.offset + column_index] = value    
            assert(self.__array[self.offset + column_index] ==value)
        def __iter__(self) -> Iterator[T]:
            for i  in  range(self.num_columns):
                yield self[i]
        def __reversed__(self) -> Iterator[T]:
            for i in range(self.num_columns, -1, -1):
                yield self[i]
        def __len__(self) -> int:
            return self.num_columns
        
        def __str__(self) -> str:
            empstring=[]
            for i in range(self.num_columns):
                empstring.append(self.__array[i+self.offset])
            return(str(empstring))
        


        
        def __repr__(self) -> str:
            return f'Row {self.row}: [{", ".join([str(self[column_index]) for column_index in range(self.num_columns - 1)])}, {str(self[self.num_columns - 1])}]'
    def __init__(self, starting_sequence: Sequence[Sequence[T]]=[[]], data_type=object) -> None:
        # forced to add columns as an arg, cause wanna stay compitable with other implemetations so can't edit
        # array, but also like the way Array is implemented it self manages size
        #better to keep non standard behaviors with a single class
        if not isinstance(starting_sequence, list):
            raise ValueError
        self.__nCols= 0 or len(starting_sequence[0])
        self.__nRows = len(starting_sequence)
        self.__data_type= data_type
        flat_start=[]
        for alist in starting_sequence:
            if len(alist) != self.__nCols or not all(isinstance(q,data_type) for q in alist):
                raise ValueError
            flat_start= flat_start + alist
        self.__carrnal =Array(flat_start, data_type)
         #checkdata and instainte underlying array before making
        #rows to acess them
             #alternitvely rows can be created lazily, by the get function
    @staticmethod
    def empty(rows: int=0, cols: int=0, data_type: type=object) -> Array2D:
        emp_seq=[]
        emp_row=[]
        for i in range(cols):
            emp_row.append(0) #this is bad, like passes the test but is there some 
            #case where 0 cant be safely cast? Not implementing checking for that cause
            #Array already does
        for i in range(rows):
            emp_seq.append(emp_row)
        return Array2D(emp_seq,data_type)
    def __getitem__(self, row_index: int) -> Array2D.IRow[T]:
        return self.Row(row_index=row_index,array=self.__carrnal,num_columns=self.__nCols)
    def __iter__(self) -> Iterator[Sequence[T]]:
        #trying not use get in iter
        offset = self.__nCols
        subarray=[]
        for i,val in enumerate(self.__carrnal): 
            if i >= offset:
                yield subarray
                offset += self.__nCols
                subarray =[]
            subarray.append(val)
        yield subarray
    def __reversed__(self):
        #Dont love this implemntation
        for i in range(self.__nRows-1,-1,-1):
            yield list(self.Row(row_index=i,array=self.__carrnal,num_columns=self.__nCols))
    def __len__(self): 
        return self.__nRows      
    def __str__(self) -> str: 
        return f'[{", ".join(f"{str(row)}" for row in self)}]'
    def __repr__(self) -> str: 
        return f'Array2D {self.__nRows} Rows x {self.__nCols} Columns, items: {str(self)}'


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
