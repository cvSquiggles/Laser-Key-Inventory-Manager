use [laserInv]

--GETS THE MOST POPULAR ORDER SIZE PER ORDER FOR EACH UNIQUE KEY NUMBER
--;WITH t1 AS
--(
--SELECT keyNum, keysUsed, count(keysUsed) countVal
--FROM ordersFilled
--GROUP BY keyNum, keysUsed
--),
--t2 AS
--(
--SELECT keyNum, max(countVal) blop
--FROM t1
--GROUP BY keyNum
--),
--t3 AS
--(
--SELECT y.keyNum, x.keysUsed
--FROM t1 x, t2 y
--WHERE blop = countVal
--GROUP BY y.keyNum, x.keysUsed
--)
--SELECT keyNum, max(keysUsed) commonOrderSize
--FROM t3
--GROUP BY keyNum

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

--GETS THE AVERAGE NUMBER OF TIMES EACH UNIQUE KEY IS ORDERED PER MONTH
--SELECT keyNum, avg(a.entry) as avgentryPerMotnh 
--FROM 
--(
--select keyNum, month(submit_time) as month, count(1) as entry 
--from ordersFilled 
--group by keyNum, month(submit_time)) a 
--GROUP BY keyNum;

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

--GETS THE NUMBER OF KEYS NEEDED TO GET THROUGH AN AVERAGE MONTH PER UNIQUE KEY
--;WITH t1 AS
--(
--SELECT keyNum, keysUsed, count(keysUsed) countVal
--FROM ordersFilled
--GROUP BY keyNum, keysUsed
--),
--t2 AS
--(
--SELECT keyNum, max(countVal) blop
--FROM t1
--GROUP BY keyNum
--),
--t3 AS
--(
--SELECT y.keyNum, x.keysUsed
--FROM t1 x, t2 y
--WHERE countVal = blop AND x.keyNum = y.keyNum
--),
--t4 AS
--(
--SELECT keyNum, commonOrderSize
--FROM
--(
--select keyNum, max(keysUsed) commonOrderSize
--FROM t3
--GROUP BY keyNum
--) a
--GROUP BY keyNum, commonOrderSize
--),
--t5 AS
--(
-- SELECT keyNum, avg(a.entry) as avgentryPerMonth 
-- FROM 
-- (
-- select keyNum, month(submit_time) as month, count(1) as entry
-- from ordersFilled 
-- group by keyNum, month(submit_time)) a 
-- GROUP BY keyNum
--),
--t6 AS
--(
-- SELECT x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth) as keysNeeded
-- FROM t4 x, t5 y
-- WHERE y.keyNum = x.keyNum
-- GROUP BY x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth)
--)
--SELECT keyNum, keysNeeded
--FROM t6
--GROUP BY keyNum, keysNeeded

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

--DOES ALL THE PREVIOUS QUERIES MATH, AND THEN LISTS THE KEY NUMBERS AND CORRESPONDING INVENTORY COUNTS WHERE SAID COUNT IS BELOW AVG NEEDED PER MONTH.
--;WITH t1 AS
--(
--SELECT keyNum, keysUsed, count(keysUsed) countVal
--FROM ordersFilled
--GROUP BY keyNum, keysUsed
--),
--t2 AS
--(
--SELECT keyNum, max(countVal) maxCountVal
--FROM t1
--GROUP BY keyNum
--),
--t3 AS
--(
--SELECT y.keyNum, x.keysUsed
--FROM t1 x, t2 y
--WHERE countVal = maxCountVal AND x.keyNum = y.keyNum
--),
--t4 AS
--(
--SELECT keyNum, commonOrderSize
--FROM
--(
--select keyNum, max(keysUsed) commonOrderSize
--FROM t3
--GROUP BY keyNum
--) a
--GROUP BY keyNum, commonOrderSize
--),
--t5 AS
--(
--SELECT keyNum, avg(a.entry) as avgentryPerMonth 
--FROM 
--(
--select keyNum, month(submit_time) as month, count(1) as entry
--from ordersFilled 
--group by keyNum, month(submit_time)) a 
--GROUP BY keyNum
--),
--t6 AS
--(
-- SELECT x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth) as keysNeeded
-- FROM t4 x, t5 y
-- WHERE y.keyNum = x.keyNum
-- GROUP BY x.keyNum, (x.commonOrderSize * y.avgEntryPerMonth)
--),
--t7 AS
--(
--SELECT *
--FROM keyInventory
--GROUP BY keyNum, invCount
--)
--SELECT x.keyNum, x.invCount, y.keysNeeded
--FROM t7 x, t6 y
--WHERE x.keyNum = y.keyNum AND x.invCount <= y.keysNeeded
--GROUP BY x.keyNum, x.invCount, y.keysNeeded;

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

--GETS THE AVERAGE # OF KEYS USED PER MONTH NOT INCLUDING THE CURRENT MONTH FOR EACH KEY.
--;WITH t1 AS
--(
-- SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
-- FROM ordersFilled x
-- WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
-- GROUP BY keyNum, submit_time, keysUsed
-- ),
-- t2 AS
-- (
-- SELECT keyNum, SUM(keysUsed) keysUsed, Date
-- FROM t1
-- GROUP BY date, keyNum
-- )
-- SELECT keyNum, AVG(keysUsed) AvgUsedPerMonth
-- FROM t2
-- GROUP BY keyNum;

 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

 --Selects from the table above all keys below the number needed to survive a month
-- ;WITH t1 AS
--(
--SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
--FROM ordersFilled x
--WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
--GROUP BY keyNum, submit_time, keysUsed
--),
--t2 AS
--(
--SELECT keyNum, SUM(keysUsed) keysUsed, Date
--FROM t1
--GROUP BY date, keyNum
--),
--t3 AS
--(
--SELECT keyNum, AVG(keysUsed) AvgUsedPerMonth
--FROM t2
--GROUP BY keyNum
--),
--t4 AS
--(
--SELECT *
--FROM keyInventory
--GROUP BY keyNum, invCount
--)
--SELECT x.keyNum, x.invCount, y.avgUsedPerMonth
--FROM t4 x, t3 y
--WHERE x.keyNum = y.keyNum AND x.invCount <= y.avgUsedPerMonth
--GROUP BY x.keyNum, x.invCount, y.avgUsedPerMonth;

 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

 --Displays keynum, current inv count, and avg needed per month for each key below said average, ALONG WITH the last time that key was ordered.
;WITH t1 AS
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
WHERE x.keyNum = y.keyNum AND x.keyNum = z.keyNum AND x.invCount <= y.avgUsedPerMonth
GROUP BY x.keyNum, x.invCount, y.avgUsedPerMonth, z.lastSubmission;