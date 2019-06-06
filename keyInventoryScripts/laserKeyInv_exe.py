#! /usr/bin/env python3

import sys
import subprocess as sp
from os import system
from utility import clear, divider, DBNAME

u_Action = None

clear()
print("Welcome to the Laser key inventory manangement tool! :D")
divider()
while True:
    u_Action = input("What would you like to do? \n\nOptions: Fill order - Resupply - Add new key - View database \n \n    ")
    if u_Action == "Fill order" or u_Action == "fill order" or u_Action == "FILL ORDER":
        import orderFill
    elif u_Action == "Resupply" or u_Action == "resupply" or u_Action == "RESUPPLY":
        import resupply
    elif "add" in u_Action or "ADD" in u_Action or "Add" in u_Action:
        import newKey
    elif "view" in u_Action or "VIEW" in u_Action or "View" in u_Action:
        import dbMenu
    elif u_Action == "quit" or u_Action == "QUIT" or "Quit" in u_Action:
        clear()
        sys.exit()
    elif u_Action == "help" or u_Action == "HELP" or u_Action == "Help":
    	clear()
    	divider()
    	print('Command Guide:\n\n'
    		'Fill order: Use this to remove keys lased from inventory.\n'
    		'\nResupply: Use this when you get new coated keys to add to inventory. \n'
            '\nAdd (new key): Use this to start tracking a new key in the database. \n'
            '\nView (database): Opens database menu where you can see inventory stats,\nand check which keys need to be ordered. \n'
    		'\nQuit: Close the program. Duh! \n')
    	divider()
    else:
        clear()
        print('Input not valid.\n'
         'TIP: If you don''t know what to type, try entering, \"help\".')
        divider()