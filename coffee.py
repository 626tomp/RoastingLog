#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


Basic classes for the input end of the program 
'''


class GreenCoffee:
    def __init__(self, name):
        self.name = name

class Blend:
    def __init__(self, name, greenCoffee):
        # greenCoffee will be an dictionary? in the form
            # {'colombia' : 80, 'nicaragua', 20}
        self.name = name
    
    def updateBlend(self, name, greenCoffee):
        self.name = name
    
