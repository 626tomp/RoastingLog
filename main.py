#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Main sequential program - for now
Mostly for testing and setting up the window 
'''

import program

# program starts here


# basic testing
testProg = program.Program()

testProg.addCoffee("Colombia")
testProg.addCoffee("Nicaragua")

#print(testProg.getCoffees())

seasonalBlend = {"Colombia": 80, "Nicaragua":20}
testProg.addBlend("Seasonal", seasonalBlend)


testProg.addCafe("Georgie Boys", "Seasonal")


