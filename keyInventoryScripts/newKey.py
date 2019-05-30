#! /usr/bin/env python3
#This is the script that adds a new key to be tracked to the key inventory

import pyodbc
import sys
from utility import clear, divider, DBNAME

#Controls all encompassing loop
moreToAdd = True

#Controls while loop to decide if the user is going to add more keys to the inventory
addMore = None

#Determines wether user has approved the information to be committed
confirmed = None

#Contains entire script, loops until user says they don't have anymore keys to add
while moreToAdd != False:
    try:
        #Prompt user for new key information
        clear()
        #Loop runs until user confirms the information they entered is correct
        while confirmed !="yes":
            print('Add a new key to the inventory by entering the key info below.')
            divider()
            u_keyNum = input('Key ID # (i.e. key #29): #')
            clear()
            print('Add a new key to the inventory by entering the key info below.')
            divider()
            u_invCount = input('How many {}''s do we have to start with? '.format(u_keyNum,))
            clear()
            #Display info and have user confirm if it's correct before continuing
            divider()
            print( " Create and track Key #{} starting at a inventory count of {}?".format(
                u_keyNum, u_invCount,) )
            divider()
            confirmed = input("Are you sure the information above is correct? ")
            #If yes then insert this information into the database
            if confirmed == 'yes':
                clear()
            elif confirmed == 'no':
                clear()
                print('Re-enter the information. \n')
            else:
                clear()
                print("Must answer yes or no, it's case sensitive because I'm lazy! \n")
        #Reset confirmed for future runs through the loop
        confirmed = "no"
        #Convert the user input to integer values for database compatibility
        u_keyNum = int(u_keyNum)
        u_invCount = int(u_invCount)
        #connect to db
        print('Connecting to database...')
        db = pyodbc.connect(Driver='{SQL Server Native Client 11.0}',
                            Server='(LocalDB)\\LocalDB Laser',
                            Database=DBNAME,
                            trusted_connection='yes')
        #Tracks wether or not there is currently an open connection to the database
        openConn = True
        #cursor 1 to ensure that the key doesn't already exist in the database
        c1 = db.cursor()
        c1.execute("SELECT keyNum FROM keyInventory WHERE keyNum = ?;", (u_keyNum,))
        #Check to see if c1 got any results, if it did, the key already exists in DB
        try:
            if (c1.fetchall()[0][0]) > 0:
                #clear()
                if openConn ==True:
                    db.close()
                    openConn = False
                divider()
                print("Error: It looks like a key with this ID # is already being tracked in the database!")
                divider()
                input("Press enter to close...")
                sys.exit()
        except IndexError:
            #clear()
            pass
        #As long as c1 didn't return anything, the code will continue
        #cursor 2 Insert the new key info into the database
        c2 = db.cursor()
        c2.execute("INSERT INTO keyInventory VALUES (?, ?);", (u_keyNum, u_invCount,))
        c2.commit()
        print("Success! This new key has been added to the database.\n")
        #Loop to ask if user would like to add more new keys to the database
        #ensure moreToAdd value is clear
        addMore = None
        while addMore != "yes" and addMore != "no":
            addMore = input("Would you like to add more new keys to the database? ")
            if addMore == 'yes':
                moreToAdd = True
            elif addMore == 'no':
                moreToAdd = False
            else:
                clear()
                print("Must answer yes or no, it's case sensitive because I'm lazy!")
    except Exception:
        #clear()
        if openConn ==True:
            db.close()
            openConn = False
        divider()
        raise
        divider()
        input("the actual end?...")
        sys.exit()
    finally:
        if openConn ==True:
            db.close()
            openConn = False
sys.exit()