#! /usr/bin/env python3

import pyodbc
import sys
import importlib
from tabulate import tabulate
from utility import clear, divider, DBNAME

invStatsQuery = '''
WITH t1 AS
(
SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
FROM ordersFilled
WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
GROUP BY keyNum, submit_time, keysUsed
),
t2 AS
(
SELECT keyNum, count(keyNum) ordersPerMonth, Date
FROM t1
GROUP BY keyNum, Date
),
t3 AS
(
SELECT keyNum, AVG(ordersPerMonth) avgOrdersPerMonth
FROM t2
GROUP BY keyNum
),
t4 AS
(
SELECT keyNum, MAX(submit_time) lastSubmission
FROM ordersFilled
GROUP BY keyNum
),
t5 AS
(
SELECT keyNum, keysUsed, COUNT(keysUsed) countVal
FROM ordersFilled
GROUP BY keyNum, keysUsed
),
t6 AS
(
SELECT keyNum, MAX(countVal) maxCountVal
FROM t5
GROUP BY keyNum
),
t7 AS
(
SELECT x.keyNum, y.keysUsed
FROM t5 y, t6 x
WHERE countVal = maxCountVal AND x.keyNum = y.keyNum
),
t8 AS
(
SELECT keyNum, commonOrderSize
FROM
(
select keyNum, max(keysUsed) commonOrderSize
FROM t7
GROUP BY keyNum
) a
GROUP BY keyNum, commonOrderSize
),
t9 AS
(
SELECT keyNum, SUM(keysUsed) totalUsed, Date
FROM t1
GROUP BY Date, keyNum
),
t10 AS
(
SELECT keyNum, AVG(totalUsed) avgTotalPerMonth
FROM t9
GROUP BY keyNum
)
SELECT a.keyNum, e.avgTotalPerMonth, d.commonOrderSize, c.avgOrdersPerMonth, b.lastSubmission
FROM t1 a, t4 b, t3 c, t8 d, t10 e
WHERE a.keyNum = b.keyNum AND b.keyNum = c.keyNum AND c.keyNum = d.keyNum AND d.keyNum = e.keyNum
GROUP BY a.keyNum, e.avgTotalPerMonth, c.avgOrdersPerMonth, d.commonOrderSize, b.lastSubmission;
'''

try:
    clear()
    print('Connecting to database...')
    db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                        Server='(LocalDB)\\LocalDB Laser',
                        Database=DBNAME,
                        trusted_connection='yes')
            
    c1 = db.cursor()
    c1.execute(invStatsQuery)
    results = c1.fetchall()
    clear()
    print(tabulate(results, headers=['Key #', 'Avg. Lased Monthly', 'Popular Order Size', 'Avg. Orders Monthly', 'Most Recent Date Lased'], tablefmt='psql'))
    input("Press enter to return to previous menu...")
    db.close()
    clear()
    import dbMenu
except Exception:
    raise
    input("Press enter to close...")
    db.close()
    sys.exit()