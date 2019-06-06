#! /usr/bin/env python3

import pyodbc
import sys
import importlib
from tabulate import tabulate
from utility import clear, divider, DBNAME

keyInvQuery = '''
SELECT * 
FROM keyInventory
GROUP BY keyNum, invCount;
'''

try:
    clear()
    print('Connecting to database...')
    db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                        Server='(LocalDB)\\LocalDB Laser',
                        Database=DBNAME,
                        trusted_connection='yes')
            
    c1 = db.cursor()
    c1.execute(keyInvQuery)
    results = c1.fetchall()
    clear()
    print(tabulate(results, headers=['Key #', 'Inventory ct.'], tablefmt='psql'))
    input("Press enter to return to previous menu...")
    db.close()
    clear()
    import dbMenu
except Exception:
    raise
    input("Press enter to close...")
    db.close()
    sys.exit()