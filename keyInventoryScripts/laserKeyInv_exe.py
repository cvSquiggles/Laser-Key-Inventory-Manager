#! /usr/bin/env python3

import sys
from os import system
import scripts
from utility import clear, divider, DBNAME

u_Action = None

#Set Large Window Size
system("mode con cols=110")

while True:
    print("Welcome to the Laser key inventory manangement tool! :D")
    divider()
    u_Action = input("What would you like to do? \n\nOptions: Fill order - Resupply - Add new key | Access Database\n \n    ")
    if "fill" in u_Action or "Fill" in u_Action or "FILL" in u_Action:
        scripts.orderFill()
    elif "re" in u_Action or "Re" in u_Action or "RE" in u_Action:
        scripts.resupply()
    elif "add" in u_Action or "ADD" in u_Action or "Add" in u_Action:
        scripts.newKey()
    elif "db" in u_Action or "DB" in u_Action or "access" in u_Action or "Access" in u_Action or "ACCESS" in u_Action:
        clear()
        scripts.dbMenu()
    elif u_Action == "quit" or u_Action == "QUIT" or "Quit" in u_Action:
        clear()
        sys.exit()
    elif u_Action == "help" or u_Action == "HELP" or u_Action == "Help":
    	clear()
    	divider()
    	print('Command Guide:\n\n'
    		'Fill (order): Use this to remove keys lased from inventory. \n'
    		'\nRe(supply): Use this when you get new coated keys to add to inventory. \n'
            '\nAdd (new key): Use this to start tracking a new key in the database. \n'
            '\nAccess (Database)\n[short cut: \'db\']: Opens database menu where you can see inventory stats,\ncheck which keys need to be ordered, etc. \n'
    		'\nQuit: Close the program. Duh! \n')
    	divider()
    else:
        clear()
        print('Input not valid.\n'
         'TIP: If you don''t know what to type, try entering, \"help\".')
        divider()