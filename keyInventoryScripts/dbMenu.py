#! /usr/bin/env python3

import sys
import subprocess as sp
from os import system
from utility import clear, divider, DBNAME, reload

#Switches to determine how scripts are loaded from this menu
lowStockCheck_Switch = False
keyInvCheck_Switch = False
statsCheck_Switch = False

clear()
print("Database: {}".format(DBNAME))
divider()
while True:
    u_Action = None
    u_Action = input("What would you like to check? \n\nOptions:  Key Inv. - Low stock keys - Key stats\n \n    ")
    if "Low" in u_Action or "low" in u_Action or "LOW" in u_Action:
        if lowStockCheck_Switch == False:
            import lowStockCheck
            clear()
            lowStockCheck_Switch = True
        else:
            clear()
            reload(lowStockCheck)
    elif "Inv" in u_Action or "inv" in u_Action or "INV" in u_Action:
        if keyInvCheck_Switch == False:
            import keyInvCheck
            clear()
            keyInvCheck_Switch = True
        else:
            clear()
            reload(keyInvCheck)
    elif "stats" in u_Action or "Stats" in u_Action or "STATS" in u_Action:
        if statsCheck_Switch == False:
            import invStats
            clear()
            statsCheck_Switch = True
        else:
            clear()
            reload(invStats)
    elif u_Action == "quit" or u_Action == "QUIT" or "Quit" in u_Action:
        clear()
        sys.exit()
    elif u_Action == "help" or u_Action == "HELP" or u_Action == "Help":
    	clear()
    	divider()
    	print('Command Guide:\n\n'
            '(Key) Inv.: Displays all keys tracked in inventory and their current inv. count. '
    		'\nLow (stock keys): Use this to check which keys need to be resupplied. \n'
            '\n(Key) Stats: Use this to view various stats for each key.'
    		'\nQuit: Close the program. Duh! \n')
    	divider()
    else:
        clear()
        print('Input not valid.\n'
         'TIP: If you don''t know what to type, try entering, \"help\".')
        divider()
sys.exit()