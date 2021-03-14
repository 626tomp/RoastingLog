#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Object for the entire program
'''

from cafe import *
from coffee import *

class Program:
    def __init__(self):
        self.cafes = []
        self.coffees = []
        self.blends = []

    def addCafe(self, cafeName, blend):
        blendName = None
        for item in self.blends:
            if (blend == item.getBlendName()):
                blendName = blend

        if (blendName == None):
            print("Blend does not exist")
            return
        
        newCafe = Cafe(cafeName, blendName)
        self.cafes.append(newCafe)
    
    def addCoffee(self, coffeeName):
        newCoffee = GreenCoffee(coffeeName)
        self.coffees.append(newCoffee)


    # make the next two functions into 1, too much repetition
    def coffeeExist(self, coffee):
        for item in self.coffees:
            #print(f'{item.getName()} vs {coffee}')
            if item.getName() == coffee:
                #print('match!')
                return True
            
        return False

    def getCoffeeObj(self, coffeeNames):
        return None 

    def addBlend(self, blendName, coffees):
        total_percentage = 0
        for key in coffees:
            total_percentage += coffees[key]
            if (not self.coffeeExist(key)):
                print("Coffee does not exist in the database")
                return
        if total_percentage != 100:
            print("Percentages need to sum to 100")
            return
        
        coffeeList = []
        for item in coffees:
            coffeeList.append(Component(item, coffees[item]))
        
        # print the blend as a check
        for item in coffeeList:
            print(f'{item.getName()} : {item.getProportion()}')

        newBlend = Blend(blendName, coffeeList)
        self.blends.append(newBlend)
    
    def getBlends(self):
        return self.blends
    
    def getCoffees(self):
        return self.coffees

    def getCafes(self):
        return self.cafes