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
                        CREATE TABLE IF NOT EXISTS GREEN (
                            g_id integer primary Key
                            name text NOT NULL
                            quantity float (quantity > 0)
                        );
                        '''

    statements = [greenCoffeeTable]
    # need to design schema

    try:
        cur = conn.cursor()
        for item in statements:
            cur.execute(item)
        print("All tables created")
    except Error as error:
        print(error)
        print("There was a problem creating the database")

def insert_green(conn, name, quantity):
    query = "INSERT INTO green values (?, ?);"
    try:
        cur = conn.cursor()
        cur.execute(query, name, quantity)
    except Error as error:
        print(error)
        print("There was a problem inserting into the database")

def update_green(conn, g_id, name, quantity):
    pass

def query_green(conn, g_id):
    pass

if __name__ == '__main__':
    pass
