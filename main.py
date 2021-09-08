#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com


'''

import database as db
import gui as g

from constants import *


if __name__ == "__main__":
    conn = db.connect_database(DATABASE_PATH)
    g.run_simple_gui(conn, {})

# do stuff here