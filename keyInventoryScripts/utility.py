#! /usr/bin/env python3
#utility functions
from os import system

#Clears the window
def clear():
    system('cls')
#Places horizontal lines in output
def divider():
    print('-' * 70)
#Database info for connections
DBNAME = "laserInv"
SVNAME = "(LocalDB)\\LocalDB Laser"
DVNAME = "{SQL Server Native Client 11.0}"