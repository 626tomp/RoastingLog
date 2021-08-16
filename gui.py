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

    return layout

if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
    layout = create_layout(conn)
    window = sg.Window("Title", layout)

    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        
        x = re.findall("-increment_\d*-", event)
        if len(x) != 0:
            x = int("".join(re.findall("\d", x[0])))
            blends = db.query_blend(conn)
            db.update_blend_quantity(conn, x, blends[x-1]['quantity'] + 5)

        x = re.findall("-decrement_\d*-", event)
        if len(x) != 0:
            x = int("".join(re.findall("\d", x[0])))
            blends = db.query_blend(conn)
            # want to find a better way to get the id
            db.update_blend_quantity(conn, x, blends[x-1]['quantity'] - 5)

        window.refresh()

    window.close()