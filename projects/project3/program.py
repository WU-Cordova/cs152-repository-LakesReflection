from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import cast

from datastructures import deque
from datastructures.array import Array
from datastructures.bag import Bag
from datastructures.deque import Deque
from extra.ansi import ansi



def main():
    class SIZES(IntEnum):
        S = -1
        M = 0
        L = 1
    @dataclass
    class Drink():
        name: str
        sizemod: float
        price: float # float cause gonna be mutipled by float
    
    @dataclass
    class Customer():
        total: float
        items: Bag
        name: str
        def __str__(self) -> str:
            cusList=[]
            for i in self.items.distinct_items():
                cusList.append("("+str(self.items.count(i)) +") "+ str(i)+"\n")
            return (self.name +"\n---\n   " + "   ".join(cusList)+"\n---\n")
    @dataclass
    class Order():
        size: str #no char type :(
        drink: Drink # should be a pointer?
        made: bool
        def __hash__(self) -> int:
            return hash(self.drink.name + self.size + str(self.made))
        def __str__(self) -> str:
            return (self.drink.name +": "+self.size)
    @dataclass
    class ICompleted(): 
        items: Bag
        total: float # mostly just bag jus this num is annoying to calc on its own

    #InLine = 0 
    # is a simple int cause before we take an order we can't have any more meaningful data than
    #they exist. Once their order is taken they get added to the queue
    Ordered = Deque(data_type=Customer)
    Completed=ICompleted(items=Bag(),total=0)
    
    drinkList=Array()
    drinkList.append(Drink(name="Rubied Sea",sizemod = 0.12,price = 8))
    drinkList.append(Drink(name="Lost in the Supermarket",sizemod =0.05,price = 9)) #everday great deals
    drinkList.append(Drink(name="Bedfellow’s Lament",sizemod = 0.20 ,price = 10))
    drinkList.append(Drink(name="But We’re Both Boys!",sizemod = 0.10,price = 13))
    drinkList.append(Drink(name="Je Serai",sizemod = 0.15,price = 10))
    #Credit to Mags for the names

    def menuOrder():
        def drinkMenu():
            ansi("2J")
            for i,val in enumerate(drinkList):
                print(i,val.name,"-",round(val.price*(1-val.sizemod),2),val.price, round(val.price*(1+val.sizemod),2))

        def orderParse(order,cust): 
            order=order.split(",")
            if any(len(i) !=2 for i in order):
                print("invalid order")
                return
            else:
                for i in order:
                    nDrink = drinkList[int(i[0])]
                    cust.total+=round((nDrink.price *(1 + (SIZES[i[1]]*(nDrink.sizemod)))),2)
                    cust.items.add(Order( 
                        drink=nDrink,
                        size=i[1],
                        made=False))

        drinkMenu()
        orItems = input("orders have the form nm,n=drink num,m=s,m,l(size) mutiple drinks are comma seperated \n").upper()
        ansi("1E", "2K")
        cust_name = input("Name for the order? \n")
        new_cust = Customer(name=cust_name, items=Bag(),total=0 )
        orderParse(orItems, new_cust)
        Ordered.enqueue(new_cust)
    
    def CompleteOrder():
        ansi("2J")
        nonlocal Completed
        finOrder = Ordered.dequeue()
        Completed.total += finOrder.total
        for i in finOrder.items.distinct_items():
            for q in range(finOrder.items.count(i)):
                Completed.items.add(i)
        print("Finshed: "+ str(finOrder))
        choice =""
        while choice != "q":
            choice=input("q to quit \n")
            ansi("1F","2K") #Move up and erase


    def CheckOrders():
        ansi("2J")
        print("OrderPrintOut")
        print( Ordered)
        choice=""
        while choice !="q":
            choice=input("q to quit \n")
            ansi("1F","2K") #Move up and erase

    def ActualTyping():
        while 1>0:
            choice =-2
            while not -1 < choice < 4:
                ansi("2J")
                choice=input('''
0. Make New Order
1. Check Open Orders
2. Close First Order
3. Exit
''')
                choice = int(choice)
            match choice:
                case 0:
                    menuOrder()
                case 1:
                    CheckOrders()
                case 2:
                    CompleteOrder()
                case 3:
                    return

    ActualTyping()

if __name__ == '__main__':
    main()
