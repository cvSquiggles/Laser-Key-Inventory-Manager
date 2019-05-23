#! /usr/bin/env python3

import sys
import subprocess as sp
from os import system

u_Action = None

def clear():
    system('clear')

clear()
print("Welcome to the Laser key inventory! :D")
print("-" * 70)
while u_Action != 'Fill order' and u_Action != 'Resupply' and u_Action != 'fill order' and u_Action != 'resupply' and u_Action != 'FILL ORDER' and u_Action != 'RESUPPLY':
    u_Action = input("What would you like to do? \nFill order - Resupply \n")
    if u_Action == 'Fill order' or u_Action == 'fill order' or u_Action == 'FILL ORDER':
        import orderFill
    elif u_Action == 'Resupply' or u_Action == 'resupply' or u_Action == 'RESUPPLY':
        import resupply
    elif u_Action == 'quit':
        clear()
        sys.exit()
    else:
        clear()
        print("Input not valid. If you don't know what to type, try entering, \"help\" next time.")
sys.exit()