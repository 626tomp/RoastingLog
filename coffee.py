#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Basic classes for the input end of the program 
'''


class GreenCoffee:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

class Blend:
    def __init__(self, name, coffeeList):
        # greenCoffee will be an dictionary? in the form
            # {'colombia' : 80, 'nicaragua', 20}
        self.name = name
        self.components = coffeeList

    def getBlendName(self):
        return self.name
    
    def updateBlend(self, name, greenCoffee):
        self.name = name

    def getCoffeeList(self):
        return self.components
    
class Component:
    def __init__(self, green, proportion):
        self.green = green
        self.proportion = proportion
    
    def getName(self):
        return self.green

    def getProportion(self):
        return self.proportion
    
