from tkinter import *
import time

import database as db

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


def getCenter(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    if screen_width < window_width:
        window_width = screen_width

    if screen_height < window_height:
        window_height = screen_height

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    return center_x, center_y, window_width, window_height

def setup():
    root = Tk()
    app = Window(root)

    # set window title
    root.wm_title("Roasting Log")

    center_x, center_y, window_width, window_height = getCenter(root, 1200, 800)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    return root
# initialize tkinter


def render(root):
    conn = db.connect_database("test.db")
    blends = db.query_blend(conn)
    #print(blends)
    test_list = ["Colombia", "Nicaragua", "Brazil"]

    for k in range(len(blends)):
        Label(root, text=blends[k]['name']).grid(row=k,column=0)
        Button(root, text="-", command=lambda a=k: update_db(conn, blends[a]['id'], blends[a]['quantity'] - 5)).grid(row=k,column=1)
        Label(root, text=blends[k]['quantity']).grid(row=k,column=2)
        Button(root, text="+", command=lambda a=k: update_db(conn, blends[a]['id'], blends[a]['quantity'] + 5)).grid(row=k,column=3)

    # Button(root, text="CLOSE WINDOW", command=lambda: close_window()).grid(row = 10, column=1)

    root.after(100, render(root))

def update_db(conn, b_id, new_quantity):

    db.update_blend_quantity(conn, b_id, new_quantity)



def close_window():
    global running
    running = False  # turn off while loop
    print( "Window closed")

if __name__ == "__main__":
    root = setup()
    render(root)

    # structure from https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
    # incl close_window()
    #root.protocol("WM_DELETE_WINDOW", close_window)
    '''running = True
    while running:
        #time.sleep(1)
        render(root)
        root.update()
        root.update_idletasks()'''

    root.mainloop()
    