## NEW ATTEMPT AT OOP
# just some practice before i commit to anything too big
import math
import sqlite3


import database


ROAST_SIZES = (4, 9, 19)

class Application:
    def __init__(self, conn):
        self.roasts = []
        self.cafes = []
        self.green = []

        # roastlist item is {roast : Roast(), roast_size : x, numRoasts : y}
        self.roast_list = []
        self.conn = conn

        # get blends from db here

    def add_new_roast(self, name):
        self.roasts.append(Roast(name, len(self.roasts)))
    
    def add_new_cafe(self, name):
        self.roasts.append(Cafe(name))

    def add_new_green(self, name):
        self.roasts.append(Green(name))

    def find_roast_with_id(self, id):
        for i in self.roasts:
            if i.get_id() == id:
                return i

    def establish_roast_list(self, list):
        # list = [(id, num), (id, num) ....]
        roast_list = []
        for i in list:
            roast = self.find_roast_with_id(i[0])
            quantity = i[1]
            if (quantity < ROAST_SIZES[0]): roast_size = ROAST_SIZES[0]
            elif (quantity < ROAST_SIZES[1]): roast_size = ROAST_SIZES[1]
            elif (quantity < ROAST_SIZES[2]): roast_size = ROAST_SIZES[2]
            num_roasts = math.ceil(quantity / roast_size)
            
            roast_list.append({'roast' : roast, 'roast_size' : roast_size, 'num_roasts' : num_roasts, 'roasts_completed' : 0})

        self.roast_list = roast_list

    def add_roast_completed(self, id):
        for i in self.roastList:
            if i['roast'].get_id() == id:
                if i['roasts_completed'] < i['num_roasts']: i['roasts_completed'] += 1
    
    def remove_roast_completed(self, id):
        for i in self.roastList:
            if i['roast'].get_id() == id:
                if i['roasts_completed'] > 0: i['roasts_completed'] -= 1


    def find_name_of_roast_with_id(self, id):
        return self.find_roast_with_id(id).get_name()




class Roast:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.components = {}
        self.postRoast = False

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def is_post_roast(self):
        return self.postRoast

    

class PostRoast(Roast):
    def __init__(self, name, id):
        super().__init__(name, id)
        self.postRoast = True



class Green:
    def __init__(self, name):
        self.name = name

    
class Cafe:
    def __init__(self, name):
        self.name = name


newApp = Application(None)

newApp.add_new_roast('id0')
newApp.add_new_roast('id1')
newApp.add_new_roast('id2')

print(newApp.find_name_of_roast_with_id(0))
print(newApp.find_name_of_roast_with_id(1))
print(newApp.find_name_of_roast_with_id(2))