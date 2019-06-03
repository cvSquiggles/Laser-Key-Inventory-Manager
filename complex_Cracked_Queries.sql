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
;WITH t1 AS
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
WHERE countVal = blop AND x.keyNum = y.keyNum
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
)
SELECT keyNum, keysNeeded
FROM t6
GROUP BY keyNum, keysNeeded