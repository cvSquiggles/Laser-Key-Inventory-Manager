#! /usr/bin/env python3

import sys
import subprocess as sp
from os import system
import importlib
from utility import clear, divider, DBNAME

lowStockCheck_Switch = False

clear()
print("Database: {}".format(DBNAME))
divider()
while True:
    u_Action = None
    u_Action = input("What would you like to check? \n\nOptions: Key Inv. - Low stock keys - Key stats - Order History \n \n    ")
    if "Low" in u_Action or "low" in u_Action or "LOW" in u_Action:
        if lowStockCheck_Switch == False:
            import lowStockCheck
            lowStockCheck_Switch = True
        else:
            importlib.reload(lowStockCheck)
    elif u_Action == "quit" or u_Action == "QUIT" or "Quit" in u_Action:
        clear()
        sys.exit()
    elif u_Action == "help" or u_Action == "HELP" or u_Action == "Help":
    	clear()
    	divider()
    	print('Command Guide:\n\n'
    		'Low (stock keys): Use this to check which keys need to be resupplied.'
    		'\nQuit: Close the program. Duh! \n')
    	divider()
    else:
        clear()
        print('Input not valid.\n'
         'TIP: If you don''t know what to type, try entering, \"help\".')
        divider()
sys.exit()