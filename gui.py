from tkinter.constants import X
import PySimpleGUI as sg
import re
import sys
from math import *

import database as db
import predict


DATABASE_PATH = "temp.db"

def update_db(conn, b_id, new_quantity):

    db.update_blend_quantity(conn, b_id, new_quantity)

def create_layout(conn):
    blends = db.query_blend(conn)
    layout = []

    for item in blends:
        layout.append([
            sg.Text(item['name']),
            sg.Button("-", size=(2, 1), key=f"-decrement_{item['id']}-"),
            sg.Input(item['quantity'], key=f"-QUANTITY_{item['id']}-"),
            sg.Button("+", size=(2, 1), key=f"-increment_{item['id']}-")
        ])

    layout.append([
            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-BLEND LIST-"),
            sg.Button("Refresh", key="-REFRESH-"), sg.Button("Edit", key="-EDIT_ENTRY-")]
        ])

    return layout

def get_formatted_blends(conn):
    blends = db.query_blend(conn)
    formatted_blends = []
    for item in blends:
        formatted_blends.append(f"{item['id']}: {item['name']} = {item['quantity']}")

    return formatted_blends

def popup_test(conn, oldValues):
    # get (or maybe get passed possible blends)
    # have drop down for 
    layout = [  [sg.Text('Update')],
            [sg.Text("Blend"), sg.OptionMenu(["Seasonal", "Hipster"],key="SELECT-BLEND")], 
            [sg.OK(), sg.Cancel()]] 
            # defaultValue=oldValues['name'] ,
    window = sg.Window("Roasting Log", layout)
    while True:             
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        if event == "OK":
            print(oldValues)
            blend = values['SELECT-BLEND']
            print(blend)
            break

        window.refresh()
    window.close()


def run_simple_gui(conn, completedToday):

    sg.theme('SystemDefault')
    blends = db.query_blend(conn)
    layout = [[
        sg.Text("Name", size = (10, 2)),
        sg.Text("KG Needed", size = (6, 2)),
        sg.Text("Remove Roast", size=(6, 2)),
        sg.Text("Roasts Left ", size = (5, 2)),
        sg.Text("Roasts Done", size = (5, 2)),
        sg.Text("Add Roast", size=(5, 2))
    ], [sg.HorizontalSeparator()]]


    for item in blends:
        id = str(item['id'])
        if not id in completedToday:
            completedToday[id] = 0
        numRoasts = ceil(item['quantity'] / 16) - completedToday[id]

        layout.append([
            sg.Text(item['name'], size = (10, 1)),
            sg.Input(item['quantity'], size = (6, 1), key=f"-QUANTITY-{id}-"),
            sg.Button("-", size=(6, 1), key=f"-decrement-{id}-"),
            sg.Text(numRoasts, size = (5, 1)),
            sg.Text(completedToday[id], size = (5, 1)),
            sg.Button("+", size=(5, 1), key=f"-increment-{id}-")
        ])
        
        if not item['postRoast']:
            contains = db.get_blend_contains(conn, item['id'])
            for component in contains:
                id = "G" + str(component['id'])
                if not id in completedToday:
                    completedToday[id] = 0
                componentQuantity = item['quantity'] * (component['percentage'] / 100)
                numRoasts = ceil(componentQuantity / 16) - completedToday[id]
                

                layout.append([
                    sg.Text("  -  " + component['name'], size = (10, 1)),
                    sg.Input(componentQuantity, size = (6, 1), key=f"-QUANTITY-{id}-"),
                    sg.Button("-", size=(6, 1), key=f"-decrement-{id}-"),
                    sg.Text(numRoasts, size = (5, 1)),
                    sg.Text(completedToday[id], size = (5, 1)),
                    sg.Button("+", size=(5, 1), key=f"-increment-{id}-")
                ])
                
    
    layout.append([sg.Button("Update", key="UPDATE"), sg.Button("Predict", key="PREDICT"), sg.Button("Reset", key="RESET")])
    window = sg.Window("Roasting Log - Simple Interface", layout)
    closed = 0
    reset = 0

    while True:            
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == "UPDATE":
            for key in completedToday:
                print(blends)
                x = re.findall("G\d*", key)
                if len(x) == 0:
                    blend = get_blend_with_id(blends, key)
                    if blend and int(values["-QUANTITY-" + key + "-"]) != blend['quantity']:
                        db.update_blend_quantity(conn, blend['id'], int(values["-QUANTITY-" + key + "-"]))
                        #print(f"values[{'-QUANTITY-' + key + '-'}] = {values['-QUANTITY-' + key + '-']} = {blend['quantity']}")
            reset = 1
        if event == "PREDICT":
            # prefill options maybe?
            predict.create_pred_window()
        if event == "RESET":
            completedToday = {}
            reset = 1


        x = re.findall("-decrement-.*-", event)
        if len(x) != 0:
            id = x[0].split("-")[2]
            if completedToday[id] > 0:
                completedToday[id] -= 1
                reset = 1
            elif completedToday[id] != 0:
                completedToday[id] = 0
                reset = 1

        x = re.findall("-increment-.*-", event)
        if len(x) != 0:
            id = x[0].split("-")[2]
            if completedToday[id] >= 0:
                completedToday[id] += 1
                reset = 1

        

        if reset == 1:
            window.close()
            run_simple_gui(conn, completedToday)
            closed = 1
            reset = 0
        window.refresh()

    if closed == 0:
        window.close()


# MOVE TO HELPER FUNCTIONS
def get_blend_with_id(blends, id):
    for item in blends:
        print(f"{item['id']} == {id}")
        if item['id'] == int(id):
            print("  returning " + str(item))
            return item
        else:
            print("  FALSE")
    
    return None

if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
    

    if len(sys.argv) >= 2 and sys.argv[1] == "simple":
        run_simple_gui(conn, {})
    else:
        layout = create_layout(conn)
        window = sg.Window("Roasting Log", layout)

        while True:             
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            
            # increment
            x = re.findall("-increment_\d*-", event)
            if len(x) != 0:
                blends = db.query_blend(conn)
                x = int("".join(re.findall("\d", x[0]))) # regex to pull off id number
                db.update_blend_quantity(conn, x, blends[x-1]['quantity'] + 5)

            # decrement
            x = re.findall("-decrement_\d*-", event)
            if len(x) != 0:
                blends = db.query_blend(conn)
                x = int("".join(re.findall("\d", x[0]))) # regex to pull off id number
                # want to find a better way to get the id
                db.update_blend_quantity(conn, x, blends[x-1]['quantity'] - 5)
                print(f"-QUANTITY_{x}-  = {blends[x-1]['quantity'] - 5}")
                values[f"-QUANTITY_{x}-"] = blends[x-1]['quantity'] - 5

            # Refresh list
            if event == "-REFRESH-":
                formatted_blends = get_formatted_blends(conn)
                window["-BLEND LIST-"].update(formatted_blends)

            # Edit
            if event == "-EDIT_ENTRY-":
                # MAKE A POP UP HERE TO EDIT THE CURRENT ENTRY
                try:
                    print("EDITING ", values["-BLEND LIST-"][0])
                    try:
                        popup_test(conn, values["-BLEND LIST-"])
                    except:
                        print("Error with popup")
                except:
                    print("You need to select an item")

            window.refresh()

        window.close()