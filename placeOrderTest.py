#! /usr/bin/env python3

from datetime import datetime
import pyodbc

DBNAME = "laserInv"

logOrder = "SELECT "

u_date = datetime.datetime.now()

try:
    u_orderNum = input('Order #:')
    u_keyNum = input('Key # used:')
    u_keysUsed = input('# of keys lased:')
    print( "{} - {} - {} ---- {}".format(
        u_keysUsed, u_keyNum, u_orderNum, u_date))
    print(type(u_orderNum))
    print(type(u_keyNum))
    print(type(u_date))
except Exception:
	raise
finally:
    print('Done')