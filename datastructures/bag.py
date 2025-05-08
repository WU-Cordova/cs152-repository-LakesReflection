from typing import Iterable, Optional
from datastructures.ibag import IBag, T

class Bag(IBag[T]):
    def __init__(self, *items: Optional[Iterable[T]]) -> None: 
        self._dict = dict ()
        for i in items:
            self.add(i)
    def add(self, item: T) -> None:
        if item:
            self._dict[item] = self._dict.setdefault(item, 0)+1
        else:
           raise TypeError('Type none may not be added a bag')
    def remove(self, item: T) -> None:
        if item in self._dict:
            holder = self._dict.pop(item)
            if holder:
                self._dict[item]=holder-1
        else:
            raise ValueError('Item is not in bag')
    def count(self, item: T) -> int:
            return self._dict.get(item) or 0
    def __len__(self) -> int:
        curlen = 0
        for i in self._dict.values():
            curlen += i
        return curlen

    def distinct_items(self) -> Iterable[T]:
        return list(self._dict)
    def __contains__(self, item) -> bool:
       return item in self._dict
    def clear(self) -> None:
       self._dict.clear()
