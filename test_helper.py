import pytest
import helper as hp
import test_database as tt

def test_calculate_needed():
    conn = tt.setup_database()
    tt.populate_database(conn)

    results = hp.calculate_needed(conn)

    print(results)

    assert(results[0]['quantity'] == -80)
    assert(results[1]['quantity'] == 80)