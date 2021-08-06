import pytest
import database as db

def setup_database():
    conn = db.connect_database('test.db')
    
    #reset db for testing
    db.drop_tables(conn)
    db.build_database(conn)

    return conn

def test_blends():
    conn = setup_database()

    db.insert_blend(conn, "Seasonal", 100)
    blends = db.query_blend(conn)

    assert(len(blends) == 1)
    assert(blends[0]['name'] == 'Seasonal')
    assert(blends[0]['quantity'] == 100)

    db.update_blend_quantity(conn, blends[0]['id'], 50)
    blends = db.query_blend(conn)

    assert(len(blends) == 1)
    assert(blends[0]['name'] == 'Seasonal')
    assert(blends[0]['quantity'] == 50)

def test_green():
    conn = setup_database()

    db.insert_green(conn, "Colombia", 100)
    greens = db.query_green(conn)

    assert(len(greens) == 1)
    assert(greens[0]['name'] == 'Colombia')
    assert(greens[0]['quantity'] == 100)

    db.update_green_quantity(conn, greens[0]['id'], 50)
    greens = db.query_green(conn)

    assert(len(greens) == 1)
    assert(greens[0]['name'] == 'Colombia')
    assert(greens[0]['quantity'] == 50)

def test_contains():
    conn = setup_database()

    db.insert_green(conn, "Colombia", 100)
    db.insert_green(conn, "Nicaragua", 100)
    db.insert_green(conn, "Brazil", 30)
    col, nic, bra = db.query_green(conn)

    db.insert_blend(conn, "Seasonal", 100)
    db.insert_blend(conn, "Hipster", 100)
    sea, hip = db.query_blend(conn)

    db.insert_contains(conn, col['id'], sea['id'], 80)
    db.insert_contains(conn, nic['id'], sea['id'], 20)

    db.insert_contains(conn, col['id'], hip['id'], 60)
    db.insert_contains(conn, bra['id'], hip['id'], 40)

    contains = db.query_contains(conn)

    print(contains)
    #return
    assert( len( contains ) == 4 )

    numCol, numNic, numBra = 0, 0, 0
    numSea, numHip = 0, 0

    for item in contains:
        if item['green'] == col['id']:
            numCol += 1
        elif item['green'] == nic['id']:
            numNic += 1
        elif item['green'] == bra['id']:
            numBra += 1
        
        if item['blend'] == sea['id']:
            numSea += 1
        elif item['blend'] == hip['id']:
            numHip += 1


    assert( numCol == 2 )
    assert( numNic == 1 )
    assert( numBra == 1 )
    assert( numHip == 2 )
    assert( numSea == 2 )
    #assert (1 == 0) # to see prints