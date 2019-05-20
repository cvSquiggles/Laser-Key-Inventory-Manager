#! /usr/bin/env python3
#This is the orderFilledScript that updates the DB when you laser keys.

from datetime import datetime
import pyodbc
import sys

DBNAME = "laserInv"

openConn = False

#pullQuery = "SELECT invCount FROM keyInventory WHERE keyNum = '{u_keyNum}'"

#insertQuery = "INSERT INTO ordersFilled ('time', 'orderNum', 'keyNum', 'keysUsed', 'preCount', 'postCount') VALUES ('')"

confirmed = None

u_date = datetime.now()

try:
    #Taking order info from user
    u_orderNum = input('Order #:')
    u_keyNum = input('Key # used:')
    u_keysUsed = input('# of keys lased:')
    #Display info and have user confirm if it's correct before committing
    while confirmed != "yes":
        print( "{} - {} - {} ---- {}".format(
            u_date, u_orderNum, u_keyNum, u_keysUsed))
        confirmed = input("Is the information above correct?")
        #If yes then insert this information into the database
        if confirmed == "yes":
            #Convert some of the user input values to int
            u_keyNum = int(u_keyNum)
            u_keysUsed = int(u_keysUsed)
            #connect to db
            db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                        Server='(LocalDB)\\LocalDB Laser',
                        Database='laserInv',
                        trusted_connection='yes')
            openConn = True
            #cursor 1 to get preCount value
            c1 = db.cursor()
            c1.execute("SELECT invCount FROM keyInventoryTEST WHERE keyNum = '%s'" % u_keyNum)
            try: 
                u_preCount = (c1.fetchall()[0][0])
            except IndexError:
                print("-" * 70)
                print("ERROR: The key number you entered doesn't exist in the keyInventory table.")
                print("TIP: If you know you've typed it correctly, you'll have to add it to the Database with newKey.py") 
            #Grab datetime for this commit
            finally:
                if openConn == True:
                    db.close()
                    openConn = False
                openConn = False
                sys.exit()

            u_date = datetime.now()
            #Calculate postCount
            u_postCount = u_preCount - u_keysUsed
            #Insert all the information into ordersFilled Table
            c2 = db.cursor()
            c2.execute("INSERT INTO ordersFilledTEST (submit_time, orderNum, keyNum, keysUsed, preCount, postCount) VALUES (?, ?, ?, ?, ?, ?)", (u_date, u_orderNum,  u_keyNum, u_keysUsed, u_preCount, u_postCount))
            c2.commit()
            #Insert the new inventory count into keyInv Table
            c3 = db.cursor()
            c3.execute("UPDATE keyInventoryTEST SET invCount = ? WHERE keyNum = ?", (u_postCount, u_keyNum))
            c3.commit()
        #If no prompt them to re-enter the information properly
        elif confirmed == "no":
            u_orderNum = input('Order #:')
            u_keyNum = input('Key # used:')
            u_keysUsed = input('# of keys lased:')
        #If they enter anything other than yes or no, ask again
        else:
            print("Must answer yes or no.")
except Exception:
	raise
finally:
    if openConn == True:
        db.close()
        openConn = False
    print('Fin')
    sys.exit()