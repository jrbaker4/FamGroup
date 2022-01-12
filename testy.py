import pandas as pd 
class foo():
    def __init__(self, poop, other_poop =2):
        self.poop = poop
        self.other_poop = other_poop
    

class bar():
    def __init__(self, poop):
        self.poop = poop
    def __eq__(self, other):
        return other.poop == self.poop

listy = [foo(0), foo(1), foo(2)]
bar1 = bar(7)
if bar1 in listy:
    print("works!")
else:
    print('sad')