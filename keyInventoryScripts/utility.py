#! /usr/bin/env python3
#utility functions
from os import system
from importlib import reload

#Clears the window
def clear():
    system('cls')
#Places horizontal lines in output
def divider():
    print('-' * 70)
#Name of database to connect to
DBNAME = "laserInv"