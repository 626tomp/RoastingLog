#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Object for the entire program

NOT USED
'''

from cafe import *
from coffee import *

class Program:
    def __init__(self):
        self.cafes = []
        self.coffees = []
        self.blends = []

    def addCafe(self, cafeName):
        newCafe = Cafe(cafeName)
        self.cafes.append(newCafe)
    
    def addCoffee(self, coffeeName):
        newCoffee = GreenCoffee(coffeeName)
        self.coffees.append(newCoffee)
    
    def addBlend(self, blendName, coffees):
        total_percentage = 0
        for greenCoffee, percentage in coffees:
            total_percentage += percentage
            pass
            # check coffee exists
        if total_percentage != 100:
            print("Percentages need to sum to 100")
            # check percentage adds to 100

            
        newBlend = Blend(blendName, coffees)
        self.blends.append(newBlend)