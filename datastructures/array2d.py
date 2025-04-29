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
            self.__array =array
            self.row =row_index
            self.offset = self.columns * self.row
        def __getitem__(self, column_index: int) -> T:
            return self.array[self.offset + column_index] #u could also do in row splices pretty easily
        def __setitem__(self, column_index: int, value: T) -> None:
            self.__array[self.offset + column_index] = value        
        def __iter__(self) -> Iterator[T]:
            for i  in  range(self.num_columns):
                yield self[i]
        def __reversed__(self) -> Iterator[T]:
            for i in range(self.num_columns, -1, -1):
                yield self[i]
        def __len__(self) -> int:
            return self.num_columns
        
        def __str__(self) -> str:
            return f"[{', '.join([str(self[column_index]) for column_index in range(self.num_columns)])}]"
        
        def __repr__(self) -> str:
            return f'Row {self.row_index}: [{", ".join([str(self[column_index]) for column_index in range(self.num_columns - 1)])}, {str(self[self.num_columns - 1])}]'


    def __init__(self, starting_sequence: Sequence[Sequence[T]]=[[]], data_type=object, columns=None) -> None:
        # forced to add columns as an arg, cause wanna stay compitable with other implemetations so can't edit
        # array, but also like the way Array is implemented it self manages size
        #better to keep non standard behaviors with a single class
        flat_start = []
        self.__num_columns= columns or len(starting_sequence[0])
        self.__num_rows = len(starting_sequence)
        for list in starting_sequence:
            if len(list) != self.__num_columns:
                raise IndexError
            flat_start += list
             ## is array argue a pointer?
            #im not sure Row even should be an object rather than a wrapper function
            #i think this how I should do this? Its better than instating @ get call I think
            # cause Row shouldn't really be holding any data, so theyre tiny?
        self.__carrnal =Array(starting_sequence, data_type)
    @staticmethod
    def empty(rows: int=0, cols: int=0, data_type: type=object) -> Array2D:
        empseq =[]
        for i in range(rows):
            empseq += [[]] #should concat
        self.__init__((empseq,data_type=data_type,columns=cols))
        # not actually emptying the array fully junk data may still exist
        return self
    def __getitem__(self, row_index: int) -> Array2D.IRow[T]:
        if row_index> self.__num_rows:
            raise IndexError
        return self.Row(row_index=row_index, array = self.__carrnal, num_columns=self.__num_columns)
    def __iter__(self) -> Iterator[Sequence[T]]: 
       return self.__carrnal 
    def __reversed__(self):
        return reversed(self.__carrnal)
    def __len__(self): 
        return len(self.__carrnal)        
    def __str__(self) -> str: 
        return f'[{", ".join(f"{str(row)}" for row in self)}]'
    
    def __repr__(self) -> str: 
        return f'Array2D {self.__num_rows} Rows x {self.__num_columns} Columns, items: {str(self)}'


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
