from math import *

import database as db
import PySimpleGUI as sg

from constants import *

def get_simple_layout(conn, completedToday):
    blends = db.query_blend(conn)
    layout = [[
        sg.Text("Name", size = (10, 2)),
        sg.Text("KG Needed", size = (6, 2)),
        sg.Text("Remove Roast", size=(6, 2)),
        sg.Text("Roasts Left ", size = (5, 2)),
        sg.Text("Roasts Done", size = (5, 2)),
        sg.Text("Add Roast", size=(5, 2))
    ], [sg.HorizontalSeparator()]]

    totalRoasts = {}
    colour = True
    for item in blends:
        id = str(item['id'])
        if not id in completedToday:
            completedToday[id] = 0
        
        if colour: background = BACKGROUND_ALTERNATE_COLOUR
        else: background = BACKGROUND_COLOUR 

        if item['postRoast']:
            numRoasts = ceil(item['quantity'] / 16)
            totalRoasts[id] = numRoasts
            if numRoasts <= completedToday[id]:
                completedToday[id] = numRoasts
            numRoasts -= completedToday[id]

            currFrame = []
            currFrame.append([
                sg.Text(item['name'], size = (10, 1), background_color=background),
                sg.Input(item['quantity'], size = (6, 1), key=f"-QUANTITY-{id}-"),
                sg.Button("-", size=(6, 1), key=f"-decrement-{id}-"),
                sg.Text(numRoasts, key=f"-numRoasts-{id}-", size = (5, 1), background_color=background),
                sg.Text(completedToday[id], key=f"-compToday-{id}-", size = (5, 1), background_color=background),
                sg.Button("+", size=(5, 1), key=f"-increment-{id}-")
            ])

            layout.append([sg.Frame("", currFrame, background_color=background, border_width=0)])
        
        else:
            
            contains = db.get_blend_contains(conn, item['id'])
            parent_id = id
            roast_sum = 0
            components = []
            for component in contains:
                id = "G" + str(component['id']) + "_" + parent_id
                if not id in completedToday:
                    completedToday[id] = 0
                componentQuantity = item['quantity'] * (component['percentage'] / 100)
                numRoasts = ceil(componentQuantity / 16)
                totalRoasts[id] = numRoasts
                if numRoasts <= completedToday[id]:
                    completedToday[id] = numRoasts
                numRoasts -= completedToday[id]
                roast_sum += completedToday[id]

                components.append([
                    sg.Text("  -  " + component['name'], size = (10, 1), background_color=background),
                    sg.Input(componentQuantity, size = (6, 1), key=f"-QUANTITY-{id}-"),
                    sg.Button("-", size=(6, 1), key=f"-decrement-{id}-"),
                    sg.Text(numRoasts, key=f"-numRoasts-{id}-", size = (5, 1), background_color=background),
                    sg.Text(completedToday[id], key=f"-compToday-{id}-", size = (5, 1), background_color=background),
                    sg.Button("+", size=(5, 1), key=f"-increment-{id}-")
                ])

            completedToday[parent_id] = roast_sum
            numRoasts = ceil(item['quantity'] / 16)
            totalRoasts[parent_id] = numRoasts
            if numRoasts <= completedToday[parent_id]:
                completedToday[parent_id] = numRoasts
            numRoasts -= completedToday[parent_id]

            currFrame = []
            currFrame.append([
                sg.Text(item['name'], size = (10, 1), background_color=background),
                sg.Input(item['quantity'], size = (6, 1), key=f"-QUANTITY-{parent_id}-"),
                sg.Button("-", size=(6, 1), button_color=DISABLED_BUTTON_COLOUR,  disabled=True, key=f"-decrement-{parent_id}-"),
                sg.Text(numRoasts, key=f"-numRoasts-{parent_id}-", size = (5, 1), background_color=background),
                sg.Text(completedToday[parent_id], key=f"-compToday-{parent_id}-", size = (5, 1), background_color=background),
                sg.Button("+", size=(5, 1), button_color=DISABLED_BUTTON_COLOUR,disabled=True, key=f"-increment-{parent_id}-")
            ])
            for item in components:
                currFrame.append(item)

            layout.append([sg.Frame("", currFrame, background_color=background, border_width=0)])

        colour = not colour # alternate colour of each row
            
    layout.append([sg.Text("Add New"), sg.Button("+", key="ADDBLEND")])
                
    roasts_rem = get_roasts_left(totalRoasts, completedToday)
    time_rem = get_time_left(roasts_rem)
    layout.append([sg.Button("Update", key="UPDATE"), sg.Button("Predict", key="PREDICT"), sg.Button("Reset", key="RESET"), 
    sg.Text(f"Roasts Left: {roasts_rem}", key="ROASTSLEFT"), 
    sg.Text(f"Time Left: {time_rem[0]}:{time_rem[1]:02d}", key="TIMELEFT")])
    return blends, completedToday, totalRoasts, layout

# MOVE TO HELPER FUNCTIONS
def get_blend_with_id(blends, id):
    for item in blends:
        #print(f"{item['id']} == {id}")
        if item['id'] == int(id):
            #print("  returning " + str(item))
            return item
    
    return None

def get_green_with_id(green, id):
    for item in green:
        #print(f"{item['id']} == {id}")
        if item['id'] == int(id):
            #print("  returning " + str(item))
            return item
    
    return None

def get_roasts_left(totalRoasts, completedToday):
    sum = 0
    for key in totalRoasts: # keys should be the same
        if "G" not in key:
            sum += totalRoasts[key]
            sum -= completedToday[key]

    return sum

def get_time_left(roast_rem):
    minutes = roast_rem * 20
    hours = floor(minutes / 60)
    minutes = minutes % 60

    return hours, minutes