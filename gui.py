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
            sg.Text(item['quantity']),
            sg.Button("+", size=(2, 1), key=f"-increment_{item['id']}-")
        ])
    test_section = [sg.Button("Refresh", key="-Add_Number-"), sg.Button("Edit", key="-EDIT_ENTRY-")]

    
    layout.append([
            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-BLEND LIST-"),
            sg.Button("Refresh", key="-Add_Number-"), sg.Button("Edit", key="-EDIT_ENTRY-")]
        ])

    return layout

if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
    layout = create_layout(conn)
    window = sg.Window("Roasting Log", layout)

    while True:             
        event, values = window.read()
        blends = db.query_blend(conn)
        formatted_blends = []
        for item in blends:
            formatted_blends.append(f"{item['id']}: {item['name']} = {item['quantity']}")


        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        
        x = re.findall("-increment_\d*-", event)
        if len(x) != 0:
            x = int("".join(re.findall("\d", x[0])))
            db.update_blend_quantity(conn, x, blends[x-1]['quantity'] + 5)

        x = re.findall("-decrement_\d*-", event)
        if len(x) != 0:
            x = int("".join(re.findall("\d", x[0])))
            # want to find a better way to get the id
            db.update_blend_quantity(conn, x, blends[x-1]['quantity'] - 5)

        if event == "-Add_Number-":
            window["-BLEND LIST-"].update(formatted_blends)

        if event == "-EDIT_ENTRY-":
            # MAKE A POP UP HERE TO EDIT THE CURRENT ENTRY
            print("EDITING ", values["-BLEND LIST-"][0])

        window.refresh()

    window.close()