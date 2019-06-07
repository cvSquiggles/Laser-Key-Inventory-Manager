#! /usr/bin/env python3

import pyodbc
import sys
import importlib
from tabulate import tabulate
from utility import clear, divider, DBNAME

modeQuery = '''
WITH t1 AS
(
SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
FROM ordersFilled x
WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
GROUP BY keyNum, submit_time, keysUsed
),
t2 AS
(
SELECT keyNum, SUM(keysUsed) keysUsed, Date
FROM t1
GROUP BY date, keyNum
),
t3 AS
(
SELECT keyNum, AVG(keysUsed) AvgUsedPerMonth
FROM t2
GROUP BY keyNum
),
t4 AS
(
SELECT *
FROM keyInventory
GROUP BY keyNum, invCount
),
t5 AS
(
SELECT keyNum, MAX(submit_time) lastSubmission
FROM ordersFilled
GROUP BY keyNum
)
SELECT x.keyNum, x.invCount, y.avgUsedPerMonth, z.lastSubmission
FROM t4 x, t3 y, t5 z
WHERE x.keyNum = y.keyNum AND x.keyNum = z.keyNum AND x.invCount <= (y.avgUsedPerMonth + 200)
GROUP BY x.keyNum, x.invCount, y.avgUsedPerMonth, z.lastSubmission;
'''

try:
    clear()
    print('Connecting to database...')
    db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                        Server='(LocalDB)\\LocalDB Laser',
                        Database=DBNAME,
                        trusted_connection='yes')
            
    c1 = db.cursor()
    c1.execute(modeQuery)
    results = c1.fetchall()
    clear()
    print(tabulate(results, headers=['Key #', 'Inventory ct.', 'Avg. per month', 'Date last lased'], tablefmt='psql'))
    input("Press enter to return to previous menu...")
    db.close()
    clear()
    import dbMenu
except Exception:
    raise
    input("Press enter to close...")
    db.close()
    sys.exit()