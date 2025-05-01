from typing import assert_type
from datastructures.array import Array, T
import os
cur_test ="START"
def main():
    dimCol = lambda : print("\033[2m",end="")
    resetCol= lambda : (print("\033[0m",end=""))
    expected = [3,2,1]
    dog = Array(expected,data_type=int)
    divider=("\n"+("─" * os.get_terminal_size().columns))
    ErrStr={
        "TYP":": Type Error on wrong type",
        "IND":": Index Error on nonexistant index",
    }
    def ErrorPrint (Err): 
        print("\033[0;92m","Success-",cur_test,ErrStr[Err])
        resetCol()

    def BeginTest (next): # just print, not actually calling any functions
        #only justifaction for that is making tracing easier + prints
        #dont run the risk of being halted by misbehaving func 
        global cur_test
        print(divider,"\033[1;94m",cur_test,"FINSHED \n", "\033[1;93m BEGIN",next,"\033[0m", divider)
        cur_test=next
        dimCol()

   
    BeginTest("APPEND") 
    for i in range(10):
        print(i,dog)
        dog.append(i)
        expected.append(i)
        assert((str(dog) == str(expected)), "\033[1;31m string rep differs from expected value \033[0m")
    try:
        dog.append("A STRING") 
    except TypeError:
        ErrorPrint("TYP")
    resetCol()
    
    BeginTest("ITERATORS")
    resetCol()
    print("\033[1m Fowards:")
    resetCol()

    for i,val in enumerate(dog):
        print(val,end=" - ")
        assert val == expected[i]
    
    print("\n \033[1m Reverse:")
    resetCol()
    for i,val in enumerate(reversed(dog)):
        print(val,end=" - ")
        assert val == expected[len(expected)-(i+1)]


    BeginTest("POP")
    while len(dog) > 0:
        print(dog.pop(), dog)
    
    #BeginTest("APPEND FRONT")

    #Pop empty list
    try:
        print(dog.pop(), dog)
    except IndexError:
        ErrorPrint("IND")

    assert((dog==expected),"Appended front did the wrong order")
    print("\033[0m") ## back to normal colors



    


if __name__ == '__main__':
    main()


