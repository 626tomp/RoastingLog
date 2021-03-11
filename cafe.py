#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Basic classes for the output end of the program 
'''

class Cafe:
    def __init__(self, name):
        self.name = name
        self.inventory = 0
        self.order = 0

    def updateInventory(self, newInventory):
        self.inventory = newInventory

    def updateOrder(self, newOrder):
        self.Order = newOrder
    
    def getName(self):
        return self.name


def testing():
    gb = Cafe('Georgie Boys')

    print(gb.getName())


# main program
testing()