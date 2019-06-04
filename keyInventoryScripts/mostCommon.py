#! /usr/bin/env python3

import pyodbc
import sys
from tabulate import tabulate
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
SELECT keyNum, max(countVal) maxCountVal
FROM t1
GROUP BY keyNum
),
t3 AS
(
SELECT y.keyNum, x.keysUsed
FROM t1 x, t2 y
WHERE countVal = maxCountVal AND x.keyNum = y.keyNum
),
t4 AS
(
SELECT keyNum, commonOrderSize
FROM
(
select keyNum, max(keysUsed) commonOrderSize
FROM t3
GROUP BY keyNum
) a
GROUP BY keyNum, commonOrderSize
),
t5 AS
(
SELECT keyNum, avg(a.entry) as avgentryPerMonth 
FROM 
(
select keyNum, month(submit_time) as month, count(1) as entry
from ordersFilled 
group by keyNum, month(submit_time)) a 
GROUP BY keyNum
),
t6 AS
(
 SELECT x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth) as keysNeeded
 FROM t4 x, t5 y
 WHERE y.keyNum = x.keyNum
 GROUP BY x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth)
),
t7 AS
(
SELECT *
FROM keyInventory
GROUP BY keyNum, invCount
)
SELECT x.keyNum, x.invCount, y.keysNeeded
FROM t7 x, t6 y
WHERE x.keyNum = y.keyNum AND x.invCount <= y.keysNeeded
GROUP BY x.keyNum, x.invCount, y.keysNeeded;
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
    print(tabulate(results, headers=['Key', 'Inventory Ct.', 'Avg. per month'], tablefmt='psql'))
    # widths = []
    # columns = []
    # tavnit = '|'
    # separator = '+' 
    # max_col_length = max(list(map(lambda x: len(str(x[1])), results)))

    # for cd in c1.description:
    #     widths.append(max(max_col_length, len(cd[0])))
    #     columns.append(cd[0])

    # for w in widths:
    #     tavnit += " %-"+"%ss |" % (w,)
    #     separator += '-'*w + '--+'

    # print(separator)
    # print(tavnit % tuple(columns))
    # print(separator)
    # for row in results:
    #     #print(tavnit, row)
    #     print(("| {:<6} |"*len(row)).format(*row))
    # print(separator)
    input("Press enter to continue...")
    db.close()
    sys.exit()
except Exception:
    raise
    input("Press enter to continue...")
    db.close()
    sys.exit()