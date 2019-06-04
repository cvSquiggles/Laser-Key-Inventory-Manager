#! /usr/bin/env python3

import pyodbc
import sys
from utility import clear, divider, DBNAME

modeQuery = '''
WITH t1 AS
(
SELECT keyNum, keysUsed, count(keysUsed) countVal
FROM ordersFilled
GROUP BY keyNum, keysUsed
),
t2 AS
(
SELECT keyNum, max(countVal) blop
FROM t1
GROUP BY keyNum
),
t3 AS
(
SELECT y.keyNum, x.keysUsed
FROM t1 x, t2 y
WHERE blop = countVal
GROUP BY y.keyNum, x.keysUsed
)
SELECT keyNum, max(keysUsed) commonOrderSize
FROM t3
GROUP BY keyNum
'''

try:
    print('Connecting to database...')
    db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                        Server='(LocalDB)\\LocalDB Laser',
                        Database=DBNAME,
                        trusted_connection='yes')
            
    c1 = db.cursor()
    c1.execute(modeQuery)
    results = c1.fetchall()
    widths = []
    columns = []
    tavnit = '|'
    separator = '+' 
    max_col_length = max(list(map(lambda x: len(str(x[1])), results)))

    for cd in c1.description:
        widths.append(max(max_col_length, len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        #print(tavnit, row)
        print(("| {:<6} |"*len(row)).format(*row))
    print(separator)
    input("Press enter to continue...")
    db.close()
    sys.exit()
except Exception:
    raise
    input("Press enter to continue...")
    db.close()
    sys.exit()