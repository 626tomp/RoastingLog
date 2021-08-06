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
                CREATE TABLE IF NOT EXISTS blends (
                    b_id integer PRIMARY KEY,
                    name text NOT NULL UNIQUE,
                    quantity integer CHECK (quantity >= 0)
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
    
    return results


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

    update_green_quantity(conn, 2, 50.5)

    results = query_green(conn)
    
    for item in results:
        if item[2] > 0:
            print(item)


    if conn:
        # save changes
        conn.commit()
        conn.close()

