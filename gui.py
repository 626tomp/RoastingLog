from tkinter.constants import X
import PySimpleGUI as sg
import re
import database as db


DATABASE_PATH = "test.db"

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

if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
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