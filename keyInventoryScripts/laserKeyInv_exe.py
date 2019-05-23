#! /usr/bin/env python3

import sys
import subprocess as sp
from os import system

u_Action = None

def clear():
    system('cls')

def divider():
	print('-' * 70)

clear()
print("Welcome to the Laser key inventory! :D")
divider()
while u_Action != 'Fill order' and u_Action != 'Resupply' and u_Action != 'fill order' and u_Action != 'resupply' and u_Action != 'FILL ORDER' and u_Action != 'RESUPPLY':
    u_Action = input("What would you like to do? \n\nOptions: Fill order - Resupply \n \n    ")
    if u_Action == 'Fill order' or u_Action == 'fill order' or u_Action == 'FILL ORDER':
        import orderFill
    elif u_Action == 'Resupply' or u_Action == 'resupply' or u_Action == 'RESUPPLY':
        import resupply
    elif u_Action == 'quit' or u_Action == 'QUIT':
        clear()
        sys.exit()
    elif u_Action == 'help' or u_Action == 'HELP' or u_Action == 'Help':
    	clear()
    	divider()
    	print('Command Guide:\n\n'
    		'Fill order: Use this to remove keys lased from inventory.\n'
    		'\nResupply: Use this when you get new coated keys to add to inventory.')
    	divider()
    else:
        clear()
        print('Input not valid.\n'
         'TIP: If you don''t know what to type, try entering, \"help\" next time.')
        divider()
sys.exit()