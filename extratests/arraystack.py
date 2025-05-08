

class ParA: 
    def __init__(self, items=None):
        self.things =None
        if items != None:
            self.__class__ = childA
    def push (self,item):
        self.things = [item]
        self.__class__ = childA

class childA(ParA): 
    def __init__(self, items):
        self.things = items
    def push (self, item):
        self.things += item
    def speak(self):
        print("woof")

dog = ParA()
dog.push(0)
print(dog)
dog.speak()
