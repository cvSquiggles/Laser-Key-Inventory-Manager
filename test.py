#! /usr/bin/env python3

import datetime
import pyodbc

DBNAME = "laserInv"

try:
    db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
    	                Server='(LocalDB)\\LocalDB Laser',
    	                Database='laserInv',
    	                trusted_connection='yes')
    c = db.cursor()
    c.execute("SELECT * FROM keyInventory")
    print(c.fetchall())
except Exception:
	raise
finally:
    db.close()
    print('Done')