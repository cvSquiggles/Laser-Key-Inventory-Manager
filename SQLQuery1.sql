use [laserInv]

--DELETE FROM ordersFilled WHERE orderNum LIKE '%; DELETE%';
--DELETE FROM resupply;
--DELETE FROM keyInventory;

--DELETE FROM resupplyTEST WHERE preCount = '9999';
--INSERT INTO resupplyTEST VALUES (00000000000, 1, 9999, 10, 9999)

--SELECT * FROM resupply;
--SELECT * FROM ordersFilled;
--SELECT * FROM keyInventory JOIN ordersFilled on keyInventory.keyNum = ordersFilled.keyNum;
--SELECT * FROM keyInventory;
--SELECT * FROM resupply;
--UPDATE keyInventory SET invCount = '1574' WHERE keyNum = '1';
--INSERT INTO keyInventory VALUES(79, 616);
--SELECT * FROM keyInventory;

--GET AVERAGE ORDER SIZE PER KEY
--SELECT keyNum, AVG(keysUsed) AS avgOrderSize FROM ordersFilled GROUP BY keyNum;

--GET AVERAGE AMOUNT OF KEY USED PER MONTH
--SELECT keyNum, (SELECT AVG(keysUsed) as avgUsedEACHmonth FROM ordersFilled GROUP BY submit_time as avgPerMonth FROM ordersFilled GROUP BY keyNum;
--SELECT keyNum, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as bump, SUM(keysUsed) from ordersFilled GROUP BY keyNum, bump;
--INSERT INTO ordersFilled VALUES ('2019-06-24 13:35:22.791', 'test', '25', '666', '60', '666')
--cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)

--Initial table
--SELECT keyNum, SUM(keysUsed) amtPerMonth, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as monat FROM ordersFilled GROUP BY keyNum, submit_time;


--The average total # of keys used per month
--SELECT a.keyNum, AVG(a.amtPerMonth) as avgPerMonth FROM (SELECT keyNum, SUM(keysUsed) amtPerMonth, (cast(month(submit_time) as varchar) + '/' + cast(year(submit_time) as varchar)) as monat FROM ordersFilled GROUP BY keyNum, submit_time) a GROUP BY keyNum;