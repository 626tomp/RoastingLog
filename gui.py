from tkinter.constants import X
import PySimpleGUI as sg
import re
import sys
from math import *

import database as db
import predict
from interface_help import *

from constants import *

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

    sg.theme('Default1')
    blends, completedToday, totalRoasts, layout = get_simple_layout(conn, completedToday)
    window = sg.Window("Roasting Log - Simple Interface", layout)
    closed = 0
    reset = 0

    while True:            
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == "UPDATE":
            for key in completedToday:
                #print(blends)
                x = re.findall("G\d*", key)
                if len(x) == 0:
                    blend = get_blend_with_id(blends, key)
                    if blend and int(values["-QUANTITY-" + key + "-"]) != blend['quantity']:
                        db.update_blend_quantity(conn, blend['id'], int(values["-QUANTITY-" + key + "-"]))
                        #print(f"values[{'-QUANTITY-' + key + '-'}] = {values['-QUANTITY-' + key + '-']} = {blend['quantity']}")
            reset = 1
        if event == "PREDICT":
            big, small = 0, 0
            for key in completedToday:
                if key[0] != 'G': 
                    curr_blend = get_blend_with_id(blends, key)
                    if curr_blend['quantity'] <= 9 and curr_blend['quantity'] > 0: small += 1
                    else: big += ceil(curr_blend['quantity'] / 16)
                
            # prefill options maybe?
            predict.create_pred_window(big, small)
        if event == "RESET":
            completedToday = {}
            reset = 1


        x = re.findall("-decrement-.*-", event)
        if len(x) != 0:
            id = x[0].split("-")[2]
            ids = id.split("_")
            if len(ids) > 1:
                parent_id = ids[1]
                if completedToday[parent_id] > 0:
                    completedToday[parent_id] -= 1
                    window[f'-numRoasts-{parent_id}-'].update(totalRoasts[parent_id] - completedToday[parent_id])
                    window[f'-compToday-{parent_id}-'].update(completedToday[parent_id])

            if completedToday[id] > 0:
                completedToday[id] -= 1
                window[f'-numRoasts-{id}-'].update(totalRoasts[id] - completedToday[id])
                window[f'-compToday-{id}-'].update(completedToday[id])
            
            roasts_rem = get_roasts_left(totalRoasts, completedToday)
            time_rem = get_time_left(roasts_rem)
            window['ROASTSLEFT'].update(f"Roasts Left: {roasts_rem}")
            window['TIMELEFT'].update(f"Time Left: {time_rem[0]}:{time_rem[1]:02d}")

        x = re.findall("-increment-.*-", event)
        if len(x) != 0:
            id = x[0].split("-")[2]
            ids = id.split("_")
            if len(ids) > 1:
                parent_id = ids[1]
                if completedToday[id] < totalRoasts[id]:
                    completedToday[parent_id] += 1
                    window[f'-numRoasts-{parent_id}-'].update(totalRoasts[parent_id] - completedToday[parent_id])
                    window[f'-compToday-{parent_id}-'].update(completedToday[parent_id])
            if completedToday[id] < totalRoasts[id]:
                completedToday[id] += 1
                window[f'-numRoasts-{id}-'].update(totalRoasts[id] - completedToday[id])
                window[f'-compToday-{id}-'].update(completedToday[id])
            
            roasts_rem = get_roasts_left(totalRoasts, completedToday)
            time_rem = get_time_left(roasts_rem)
            window['ROASTSLEFT'].update(f"Roasts Left: {roasts_rem}")
            window['TIMELEFT'].update(f"Time Left: {time_rem[0]}:{time_rem[1]:02d}")

        

        if reset == 1:
            window.close()
            #recursively launch the window again with the new info
            run_simple_gui(conn, completedToday)
            closed = 1
            reset = 0
        window.refresh()

    if closed == 0:
        window.close()


# simplfy and move stuff to other functions
# move main to another file
if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
    

    if len(sys.argv) >= 2 and sys.argv[1] == "full":
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
    else:
        run_simple_gui(conn, {})