import database as db

def calculate_needed(conn):
    ''' 
    queries the db for cafes and blends. Returns a dictionary very similar to
    the db schema for the blends, but with the volume decremented by the amount
    of that blend needed for the cafes listed.
    '''

    cafes = db.query_cafe(conn)
    blends = db.query_blend(conn)

    for i in range(len(blends)):
        
        for cafe in cafes:
            print("here")
            if cafe['blend'] == blends[i]['id']:
                print("here")
                blends[i]['quantity'] -= cafe['volume']

    return blends

