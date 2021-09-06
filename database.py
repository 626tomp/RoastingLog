#!/usr/bin/python3
'''
Written by Thomas Parish
Contact: 1tomparish@gmail.com

Where all the database tables are setup and where all the interaction with the 
database occurs
'''
import sqlite3
from sqlite3 import Error



def connect_database(db_file):
    '''
    Takes in a File, returns the connection to the database at that filepath
    Will create a database if no file exists at that filepath
    '''
    try:
        # If new connection required
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def build_database(conn):
    '''builds database if it doesnt exist yet, should only run once'''

    greenCoffeeTable = '''
                        CREATE TABLE IF NOT EXISTS green (
                            g_id integer primary Key,
                            name text NOT NULL  UNIQUE,
                            quantity float CHECK (quantity >= 0)
                        );
                        '''

    blendTable = '''
                CREATE TABLE IF NOT EXISTS blend (
                    b_id integer PRIMARY KEY,
                    name text NOT NULL UNIQUE,
                    quantity integer CHECK (quantity >= 0),
                    postRoast integer CHECK (postRoast >= 0 and postRoast <= 1)
                );
                '''

    blendContainsTable = '''
                        CREATE TABLE IF NOT EXISTS contains (
                            green integer NOT NULL,
                            blend integer NOT NULL,
                            percentage float NOT NULL CHECK (percentage > 0 AND percentage <= 100),
                            PRIMARY KEY (green, blend),
                            FOREIGN KEY(green) REFERENCES green(g_id),
                            FOREIGN KEY(blend) REFERENCES blends(b_id)
                        );
                        '''
    
    cafeTable = '''
                CREATE TABLE IF NOT EXISTS cafe (
                    c_id integer PRIMARY KEY,
                    name text NOT NULL UNIQUE,
                    blend integer NOT NULL,
                    volume integer CHECK (volume > 0),
                    FOREIGN KEY(blend) REFERENCES blends(b_id)
                );
                '''

    statements = [greenCoffeeTable, blendTable, blendContainsTable, cafeTable]
    # need to design schema

    try:
        cur = conn.cursor()
        print("Starting table creation")
        for item in statements:
            print("     Created table")
            cur.execute(item)
        print("All tables created")
    except Error as error:
        print(error)
        print("There was a problem creating the database")

def insert_green(conn, name, quantity):
    query = "INSERT INTO green values (?, ?, ?);"
    try:
        cur = conn.cursor()
        cur.execute(query, (None, name, quantity))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem inserting into the database")

def update_green_quantity(conn, g_id, quantity):
    query = "UPDATE green set quantity = ? where g_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (quantity, g_id))
    except Error as error:
        print(error)
        print("There was a problem updating the green quantity")
    
def update_green_name(conn, g_id, name):
    query = "UPDATE green set name = ? where g_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (name, g_id))
    except Error as error:
        print(error)
        print("There was a problem updating the green name")

def query_green(conn):
    query = "select * from green;"
    try:
        cur = conn.cursor()
        results = cur.execute(query)
    except Error as error:
        print(error)
        print("There was a problem querying the green table")
    
    values = []
    for item in results:
        curr = {}
        curr['id'] = item[0]
        curr['name'] = item[1]
        curr['quantity'] = item[2]
        values.append(curr)

    return values

def insert_blend(conn, name, quantity, postRoast):
    query = "INSERT INTO blend values (?, ?, ?, ?);"
    try:
        cur = conn.cursor()
        cur.execute(query, (None, name, quantity, postRoast))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem inserting into the database")

def update_blend_quantity(conn, b_id, quantity):
    query = "UPDATE blend set quantity = ? where b_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (quantity, b_id))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem updating the blend quantity")
    
def update_blend_name(conn, b_id, name):
    query = "UPDATE blend set name = ? where b_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (name, b_id))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem updating the blend name")

def query_blend(conn):
    query = "select * from blend;"
    try:
        cur = conn.cursor()
        results = cur.execute(query)
    except Error as error:
        print(error)
        print("There was a problem querying the blend table")
    
    values = []
    for item in results:
        curr = {}
        curr['id'] = item[0]
        curr['name'] = item[1]
        curr['quantity'] = item[2]
        curr['postRoast'] = item[3]
        values.append(curr)

    return values

def insert_contains(conn, green, blend, percentage):
    query = "INSERT INTO contains values (?, ?, ?);"
    try:
        cur = conn.cursor()
        cur.execute(query, (green, blend, percentage))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem inserting into the database")

def update_contains_percentage(conn, blend, green, percentage):
    query = "UPDATE contains set percentage = ? where blend = ? AND green = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (percentage, blend, green))
    except Error as error:
        print(error)
        print("There was a problem updating the contains quantity")
    
def update_contains_green(conn, blend, green):
    query = "UPDATE contains set green = ? where blend = ? and green = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (green, blend, green))
    except Error as error:
        print(error)
        print("There was a problem updating the contains name")

def query_contains(conn):
    query = "select * from contains;"
    try:
        cur = conn.cursor()
        results = cur.execute(query)
    except Error as error:
        print(error)
        print("There was a problem querying the contains table")
    
    values = []
    for item in results:
        curr = {}
        curr['green'] = item[0]
        curr['blend'] = item[1]
        curr['percentage'] = item[2]
        values.append(curr)

    return values

def insert_cafe(conn, name, blend, volume):
    query = "INSERT INTO cafe values (?, ?, ?, ?);"
    try:
        cur = conn.cursor()
        cur.execute(query, (None, name, blend, volume))
        conn.commit()
    except Error as error:
        print(error)
        print("There was a problem inserting into the database")

def update_cafe_blend(conn, c_id, blend):
    query = "UPDATE cafe set blend = ? where c_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (blend, c_id))
    except Error as error:
        print(error)
        print("There was a problem updating the contains quantity")
    
def update_cafe_name(conn, c_id, name):
    query = "UPDATE cafe set name = ? where c_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (name, c_id))
    except Error as error:
        print(error)
        print("There was a problem updating the cafe name")

def update_cafe_volume(conn, c_id, volume):
    query = "UPDATE cafe set volume = ? where c_id = ?;"
    try:
        cur = conn.cursor()
        cur.execute(query, (volume, c_id))
    except Error as error:
        print(error)
        print("There was a problem updating the cafe volume")

def query_cafe(conn):
    query = "select * from cafe;"
    try:
        cur = conn.cursor()
        results = cur.execute(query)
    except Error as error:
        print(error)
        print("There was a problem querying the cafe table")
    
    values = []
    for item in results:
        curr = {}
        curr['id'] = item[0]
        curr['name'] = item[1]
        curr['blend'] = item[2]
        curr['volume'] = item[3]
        values.append(curr)

    return values
    
def get_blend_contains(conn, b_id):
    query = '''
            SELECT g.g_id, g.name, c.percentage, b.b_id from green g
            JOIN contains c on (g.g_id = c.green)
            JOIN blend b on (b.b_id = c.blend)
            WHERE b.b_id = ?;
            '''
    try:
        cur = conn.cursor()
        results = cur.execute(query, (b_id,))
    except Error as error:
        print(error)
        print("There was a problem joining the cafe table")
    
    values = []
    for item in results:
        curr = {}
        curr['id'] = item[0]
        curr['name'] = item[1]
        curr['percentage'] = item[2]
        curr['blend_id'] = item[3]
        values.append(curr)

    return values

def drop_tables(conn):
    
    query1 = "DROP TABLE IF EXISTS green;"
    query2 = "DROP TABLE IF EXISTS contains;"
    query3 = "DROP TABLE IF EXISTS cafe;"
    query4 = "DROP TABLE IF EXISTS blend;"
    queries = [query1, query2, query3, query4]
    try:
        cur = conn.cursor()
        for item in queries:
            cur.execute(item)
    except Error as error:
        print(error)
        print("There was a problem deleting tables")
    

if __name__ == '__main__':
    conn = connect_database('data.db')
    
    #reset db for testing
    drop_tables(conn)
    build_database(conn)

    insert_green(conn, "Colombia Matambo", 0.0)
    insert_green(conn, "Colombia El Pariso", 0.0)
    insert_green(conn, "Nicaragua La Trampa", 15)


    results = query_green(conn)
    
    insert_blend(conn, "Seasonal", 100, 1)
    insert_blend(conn, "Hipster", 45, 0)
    insert_blend(conn, "Decaf", 6, 0)


    if conn:
        # save changes
        conn.commit()
        conn.close()

