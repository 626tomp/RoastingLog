#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Basic classes for the output end of the program 
'''

class Cafe:
    def __init__(self, name, blend):
        self.name = name
        self.inventory = 0
        self.order = 0
        self.needed = 0
        self.blend = blend

    def updateInventory(self, newInventory):
        self.inventory = newInventory
        self.updateNeeded()

    def updateOrder(self, newOrder):
        self.Order = newOrder
    
    def getName(self):
        return self.name

    def updateNeeded(self):
        toRoast = self.order - self.inventory
        if(toRoast > 0):
            self.needed = toRoast