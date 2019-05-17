use [laserInv]

--DELETE FROM ordersFilledTEST;

SELECT * FROM keyInventoryTEST JOIN ordersFilledTEST on keyInventoryTEST.keyNum = ordersFilledTEST.keyNum;
--SELECT * FROM keyInventoryTEST;