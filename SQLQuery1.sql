use [laserInv]

--DELETE FROM ordersFilled WHERE orderNum LIKE 'test';
--DELETE FROM resupply;
--DELETE FROM keyInventory WHERE keyNum = '89995';

--GET AVERAGE ORDER SIZE PER KEY
--SELECT keyNum, AVG(keysUsed) AS avgOrderSize FROM ordersFilled GROUP BY keyNum;

--GET AVERAGE AMOUNT OF KEY USED PER MONTH
--SELECT keyNum, (SELECT AVG(keysUsed) as avgUsedEACHmonth FROM ordersFilled GROUP BY submit_time as avgPerMonth FROM ordersFilled GROUP BY keyNum;
--SELECT keyNum, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as bump, SUM(keysUsed) from ordersFilled GROUP BY keyNum, bump;
--INSERT INTO ordersFilled VALUES ('2019-06-24 13:35:22.791', 'test', '25', '666', '60', '666')
--cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)

--Initial table
--SELECT keyNum, keysUsed, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as month FROM ordersFilled GROUP BY keyNum, keysUsed, submit_time ORDER BY keyNum, keysUsed;



--SELECT keyNum, keysUsed, count(keyNum) valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed ORDER BY keyNum, valueOccurence;


--The average total # of keys used per ORDER
--SELECT a.keyNum, AVG(a.keysUsed) as avgPerOrder FROM (SELECT keyNum, keysUsed, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as month FROM ordersFilled GROUP BY keyNum, keysUsed, submit_time) a GROUP BY keyNum;
--SELECT a.keyNum, AVG(a.numPerOrder) as avgPerOrder FROM (SELECT keyNum, SUM(keysUsed) as numPerOrder, orderNum FROM ordersFilled GROUP BY keyNum, keysUsed, orderNum) a GROUP BY keyNum;

--This query aggregates the # of keys used of each key num logged on an order, and displays how many times that amount was ordered.  This shows how many to expect on an order.
--SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed ORDER BY keyNum, valueOccurence DESC;

--SELECT a.keyNum, MAX(a.keysUsed) FROM (SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) a GROUP BY keyNum;

--SELECT o.keyNum, o.keysUsed FROM (SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) o JOIN (SELECT MAX(valueOccurence) maxValue FROM (SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) i where valueOccurence = maxValue;

--SELECT i.keyNum, i.keysUsed FROM ((SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) i join (SELECT MAX(valueOccurence) as maxValue FROM (SELECT keyNum, keysUsed, count(keysUsed) as valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) a) x HAVING valueOccurence = maxValue GROUP BY i.keyNum;


----------------------------------------------------------------------------------------------------------------------------------------------------------

--SELECT keyNum, keysUsed, count(keyNum) valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed ORDER BY keyNum, valueOccurence;

--SELECT MAX (x.valueOccurence) maxValue FROM (SELECT keyNum, keysUsed, count(keyNum) valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) x;

--SELECT TOP 1 WITH TIES keyNum, keysUsed, MAX (x.valueOccurence) maxValue FROM (SELECT keyNum, keysUsed, count(keyNum) valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) x GROUP BY keyNum, keysUsed ORDER BY maxValue DESC;

--SELECT TOP (1) WITH TIES keyNum, keysUsed, max_valueOccurence FROM (SELECT keyNum, keysUsed, count(keysUsed) as max_valueOccurence FROM ordersFilled GROUP BY keyNum, keysUsed) x WHERE max_valueOccurence in (SELECT max(count_val) FROM (SELECT keyNum, keysUsed, count(keysUsed) as count_val from ordersFilled GROUP BY keyNum, keysUsed) y) GROUP BY keyNum, keysUsed, max_valueOccurence ORDER BY keyNum, keysUsed;
--SELECT max(count_val) FROM (SELECT keyNum, keysUsed, count(keysUsed) as count_val from ordersFilled GROUP BY keyNum, keysUsed) x;

--;WITH keyAvgOrder AS
--(
--SELECT keyNum, keysUsed, COUNT(keysUsed) as valueOccurence
--FROM ordersFilled
--GROUP BY keyNum, keysUsed
--),
--keyAvgOrderRank AS
--(
--SELECT keyNum, keysUsed, max(valueOccurence) maxim
--FROM keyAvgOrder
--GROUP BY keyNum, keysUsed, valueOccurence
--)
--SELECT a.keyNum, a.keysUsed, a.maxim
--FROM keyAvgOrderRank a, keyAvgOrder b
--WHERE maxim = valueOccurence;

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
WHERE blop = countVal
GROUP BY y.keyNum, x.keysUsed
)
SELECT keyNum, max(keysUsed) commonOrderSize
FROM t3
GROUP BY keyNum

