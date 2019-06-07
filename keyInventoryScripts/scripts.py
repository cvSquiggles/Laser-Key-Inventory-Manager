#! /usr/bin/env python3

import pyodbc
import sys
import scripts
from datetime import datetime
from tabulate import tabulate
from utility import clear, divider, DBNAME, SVNAME, DVNAME

def invStats():
    invStatsQuery = '''
    WITH t1 AS
    (
    SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
    FROM ordersFilled
    WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
    GROUP BY keyNum, submit_time, keysUsed
    ),
    t2 AS
    (
    SELECT keyNum, count(keyNum) ordersPerMonth, Date
    FROM t1
    GROUP BY keyNum, Date
    ),
    t3 AS
    (
    SELECT keyNum, AVG(ordersPerMonth) avgOrdersPerMonth
    FROM t2
    GROUP BY keyNum
    ),
    t4 AS
    (
    SELECT keyNum, MAX(submit_time) lastSubmission
    FROM ordersFilled
    GROUP BY keyNum
    ),
    t5 AS
    (
    SELECT keyNum, keysUsed, COUNT(keysUsed) countVal
    FROM ordersFilled
    GROUP BY keyNum, keysUsed
    ),
    t6 AS
    (
    SELECT keyNum, MAX(countVal) maxCountVal
    FROM t5
    GROUP BY keyNum
    ),
    t7 AS
    (
    SELECT x.keyNum, y.keysUsed
    FROM t5 y, t6 x
    WHERE countVal = maxCountVal AND x.keyNum = y.keyNum
    ),
    t8 AS
    (
    SELECT keyNum, commonOrderSize
    FROM
    (
    select keyNum, max(keysUsed) commonOrderSize
    FROM t7
    GROUP BY keyNum
    ) a
    GROUP BY keyNum, commonOrderSize
    ),
    t9 AS
    (
    SELECT keyNum, SUM(keysUsed) totalUsed, Date
    FROM t1
    GROUP BY Date, keyNum
    ),
    t10 AS
    (
    SELECT keyNum, AVG(totalUsed) avgTotalPerMonth
    FROM t9
    GROUP BY keyNum
    )
    SELECT a.keyNum, e.avgTotalPerMonth, d.commonOrderSize, c.avgOrdersPerMonth, b.lastSubmission
    FROM t1 a, t4 b, t3 c, t8 d, t10 e
    WHERE a.keyNum = b.keyNum AND b.keyNum = c.keyNum AND c.keyNum = d.keyNum AND d.keyNum = e.keyNum
    GROUP BY a.keyNum, e.avgTotalPerMonth, c.avgOrdersPerMonth, d.commonOrderSize, b.lastSubmission;
    '''

    try:
        clear()
        print('Connecting to database...')
        db = pyodbc.connect(Driver= DVNAME,
                            Server= SVNAME,
                            Database=DBNAME,
                            trusted_connection='yes')               
        c1 = db.cursor()
        c1.execute(invStatsQuery)
        results = c1.fetchall()
        clear()
        print(tabulate(results, headers=['Key #', 'Avg. Lased Monthly', 'Popular Order Size', 'Avg. Orders Monthly', 'Most Recent Date Lased'], tablefmt='psql'))
        input("Press enter to return to previous menu...")
        db.close()
        clear()
    except Exception:
        raise
        input("Press enter to close...")
        db.close()

def keyInvCheck():
    keyInvQuery = '''
    SELECT * 
    FROM keyInventory
    GROUP BY keyNum, invCount;
    '''

    try:
        clear()
        print('Connecting to database...')
        db = pyodbc.connect(Driver= DVNAME,
                            Server= SVNAME,
                            Database=DBNAME,
                            trusted_connection='yes')      
        c1 = db.cursor()
        c1.execute(keyInvQuery)
        results = c1.fetchall()
        clear()
        print(tabulate(results, headers=['Key #', 'Inventory ct.'], tablefmt='psql'))
        input("Press enter to return to previous menu...")
        db.close()
        clear()
    except Exception:
        raise
        input("Press enter to close...")
        db.close()

def lowStockCheck():
    modeQuery = '''
    WITH t1 AS
    (
    SELECT keyNum, keysUsed, CONVERT(CHAR(7),submit_time,120) Date
    FROM ordersFilled x
    WHERE CONVERT(CHAR(7),submit_time,120) != CONVERT(CHAR(7),GETDATE(),120)
    GROUP BY keyNum, submit_time, keysUsed
    ),
    t2 AS
    (
    SELECT keyNum, SUM(keysUsed) keysUsed, Date
    FROM t1
    GROUP BY date, keyNum
    ),
    t3 AS
    (
    SELECT keyNum, AVG(keysUsed) AvgUsedPerMonth
    FROM t2
    GROUP BY keyNum
    ),
    t4 AS
    (
    SELECT *
    FROM keyInventory
    GROUP BY keyNum, invCount
    ),
    t5 AS
    (
    SELECT keyNum, MAX(submit_time) lastSubmission
    FROM ordersFilled
    GROUP BY keyNum
    )
    SELECT x.keyNum, x.invCount, y.avgUsedPerMonth, z.lastSubmission
    FROM t4 x, t3 y, t5 z
    WHERE x.keyNum = y.keyNum AND x.keyNum = z.keyNum AND x.invCount <= (y.avgUsedPerMonth + 200)
    GROUP BY x.keyNum, x.invCount, y.avgUsedPerMonth, z.lastSubmission;
    '''

    try:
        clear()
        print('Connecting to database...')
        db = pyodbc.connect(Driver= DVNAME,
                            Server= SVNAME,
                            Database=DBNAME,
                            trusted_connection='yes')        
        c1 = db.cursor()
        c1.execute(modeQuery)
        results = c1.fetchall()
        clear()
        print(tabulate(results, headers=['Key #', 'Inventory ct.', 'Avg. per month', 'Date last lased'], tablefmt='psql'))
        input("Press enter to return to previous menu...")
        db.close()
        clear()
    except Exception:
        raise
        input("Press enter to close...")
        db.close()

def orderFill():
    openConn = False

    #Determines wether the user has confirmed the information was typed correctly
    confirmed = None

    #Determines wether the code should loop for more key entries
    orderComplete = False

    #Marks that it's not the first loop, so don't ask for order number again
    multiKeyOrder = False

    #Used to navigate loop where user decides to loop code or not
    addMore = None

    u_date = datetime.now()

    while orderComplete == False:
        try:
            #Taking order info from user
            clear()
            while confirmed != "yes":
                print('Update the key inventory by entering the order information below.')
                divider()
                if multiKeyOrder == False:
                    u_orderNum = input('Order #: ')
                u_keyNum = input('Key used (i.e. #29): #')
                u_keysUsed = input('# of keys lased: ')
                clear()
                #Display info and have user confirm if it's correct before committing
                divider()
                print( "Lase {} key {}'s for order {} on {}?".format(
                    u_keysUsed, u_keyNum, u_orderNum, u_date))
                divider()
                confirmed = input("Is the information above correct? ")
                #If yes then insert this information into the database
                if confirmed == "yes":
                    clear()
                #If no prompt them to re-enter the information properly
                elif confirmed == "no":
                    clear()
                    print('Re-enter the information. \n')
                #If they enter anything other than yes or no, ask again
                else:
                    clear()
                    print("Must answer yes or no, it's case sensitive because I'm lazy! \n")
            #Reset confirmed for future while loops
            confirmed = "no"
            #Convert some of the user input values to int
            u_keyNum = int(u_keyNum)
            u_keysUsed = int(u_keysUsed)
            #connect to db
            print('Connecting to database...')
            db = pyodbc.connect(Driver= DVNAME,
                                Server= SVNAME,
                                Database=DBNAME,
                                trusted_connection='yes')
            openConn = True
            #cursor 1 to get preCount value
            c1 = db.cursor()
            c1.execute("SELECT invCount FROM keyInventory WHERE keyNum = '%s';" % (u_keyNum,))
            try: 
                #Check to see if cursor one has A result.
                u_preCount = (c1.fetchall()[0][0])
            except IndexError:
                divider()
                print("ERROR: The key number you entered doesn't exist in the keyInventory table.")
                print("TIP: If you know you've typed it correctly, you'll have to add it to the Database with newKey.py") 
                divider()
                input("Press Enter to close...")
                if openConn == True:
                    db.close()
                    openConn = False
                sys.exit()
            except Exception:
                if openConn == True:
                    db.close()
                    openConn = False
                    divider()
                    raise
                    divider()
                    input("Press Enter to close...")
                sys.exit()
            #Grab datetime for this commit
            u_date = datetime.now()
            #Calculate postCount
            u_postCount = u_preCount - u_keysUsed
            #Insert all the information into ordersFilled Table
            c2 = db.cursor()
            c2.execute("INSERT INTO ordersFilled (submit_time, orderNum, keyNum, keysUsed, preCount, postCount) VALUES (?, ?, ?, ?, ?, ?);", (u_date, u_orderNum,  u_keyNum, u_keysUsed, u_preCount, u_postCount,))
            c2.commit()
            #Insert the new inventory count into keyInv Table
            c3 = db.cursor()
            c3.execute("UPDATE keyInventory SET invCount = ? WHERE keyNum = ?;", (u_postCount, u_keyNum,))
            c3.commit()
            clear()
            print('Success! Database has been updated.')
            addMore = None
            #While loop to ask user if they want to remove more keys from inventory
            while addMore != "yes" and addMore != "no": 
                addMore = input('Are there more keys on this order? ')
                if addMore == 'yes':
                    multiKeyOrder = True
                    if openConn == True:
                        db.close()
                        openConn = False
                elif addMore == 'no':
                    orderComplete = True
                    clear()
                else:
                    clear()
                    print("Must answer yes or no, it's case sensitive because I'm lazy!")
        except Exception:
            raise
        finally:
            if openConn == True:
                db.close()
                openConn = False\

def resupply():
    #This variable is used throughout the code to track wether the connection is still
    #open, and generally that check will close it and set to false if it is.
    openConn = False

    #Bool to determine wether code should loop or not.
    resupplyComplete = False

    #Bool to confirm user input is correct.
    confirmed = None

    #Determines wether user wants to add more keys to inventory.
    addMore = None

    #If encapsulates the code, re-runs it if you say you want to enter more resupply info.
    while resupplyComplete == False:
        try:
            clear()
            print('Update the key inventory by entering the key resupply info below.')
            divider()
            u_keyNum = input('Key # to add (i.e. Key #29): #')
            u_keysAdded = input('# of keys to add to inventory: ')
            clear()
            while confirmed != "yes":
                divider()
                print( "Adding {} key {}'s to the inventory. \nIs this correct?".format(u_keysAdded, u_keyNum))
                divider()
                confirmed = input('Please enter ''yes'' or ''no'': ')
                if confirmed == "yes":
                    #Do nothing
                    clear()
                elif confirmed == "no":
                    clear()
                    print('Re-enter the information.')
                    u_keyNum = input('Key # used (i.e. Key #29): #')
                    u_keysAdded = input('# of keys to add to inventory:')
                else:
                    clear()
                    print("Must answer yes or no, it's case sensitive because I'm lazy!")
            #If yes then proceed to insert this information into the database
            #First reset confirmed status in case user adds more keys later.
            confirmed = "no"
            #Convert user input values to type int
            u_keyNum = int(u_keyNum)
            u_keysAdded = int(u_keysAdded)
            #connect to db
            print('Connecting to database...')
            db = pyodbc.connect(Driver= DVNAME,
                                Server= SVNAME,
                                Database=DBNAME,
                                trusted_connection='yes')
            openConn = True
            #cursor 1 to get preCount value
            c1 = db.cursor()
            c1.execute("SELECT invCount FROM keyInventory WHERE keyNum = '%s';" % (u_keyNum,))
            try:
                #Check to see if cursor has A result
                u_preCount = (c1.fetchall()[0][0])
            except IndexError:
                #If sql select statement gets no result
                divider()
                print("ERROR: The key number you entered doesn't exist in the keyInventory table.")
                print("TIP: If you know you've typed it correctly, you'll have to add it to the Database with newKey.py") 
                divider()
                input("Press enter to close...")
                if openConn == True:
                    db.close() 
                    openConn = False
                sys.exit()
            except Exception:
                #All other exceptions
                if openConn == True:
                    db.close()
                    openConn = False
                divider()
                raise
                divider()
                input("Press enter to close...")
                sys.exit()
            #If Sql result DOES contain a result, get datetime for this resupply
            u_date = datetime.now()
            #Calculate post resupply Count
            u_postCount = u_preCount + u_keysAdded
            #Insert the resupply information into the resupply table
            c2 = db.cursor()
            c2.execute("INSERT INTO resupply (submit_time, keyNum, keysAdded, preCount, postCount) VALUES (?, ?, ?, ?, ?);", (u_date, u_keyNum, u_keysAdded, u_preCount, u_postCount,))
            c2.commit()
            #Update the new inventory count into keyInv Table
            c3 = db.cursor()
            c3.execute("UPDATE keyInventory SET invCount = ? WHERE keyNum = ?;", (u_postCount, u_keyNum,))
            c3.commit()
            print('Success! Database has been updated.')
            divider()
            addMore = None
            while addMore != "yes" and addMore != "no": 
                addMore = input('Would you like to add more keys to the inventory? ')
                if addMore == 'yes':
                    #do nothing
                    if openConn == True:
                        db.close()
                        openConn = False
                elif addMore == 'no':
                    resupplyComplete = True;
                    clear()
                else:
                    clear()
                    print("Must answer yes or no, it's case sensitive because I'm lazy!")
        except Exception:
            if openConn == True:
                db.close()
                openConn = False
            divider()
            raise
            divider()
            input("Press enter to close...")
            sys.exit()
        finally:
            if openConn == True:
                db.close()
                openConn = False

def newKey():
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
            db = pyodbc.connect(Driver= DVNAME,
                                Server= SVNAME,
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
            divider()
            #Loop to ask if user would like to add more new keys to the database
            #ensure moreToAdd value is clear
            addMore = None
            while addMore != "yes" and addMore != "no":
                addMore = input("Would you like to add more new keys to the database? ")
                if addMore == 'yes':
                    moreToAdd = True
                elif addMore == 'no':
                    moreToAdd = False
                    clear()
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
            sys.exit()
        finally:
            if openConn ==True:
                db.close()
                openConn = False

def dbMenu():
    dbMenu = True

    while dbMenu == True:
        print("Database: {}".format(DBNAME))
        divider()
        u_Action = None
        u_Action = input("What would you like to check? \n\nOptions:  Key Inv. - Low stock keys - Key stats | Back\n \n    ")
        if "Low" in u_Action or "low" in u_Action or "LOW" in u_Action:
                lowStockCheck()
        elif "Inv" in u_Action or "inv" in u_Action or "INV" in u_Action:
                keyInvCheck()
        elif "stats" in u_Action or "Stats" in u_Action or "STATS" in u_Action:
                invStats()
        elif "back" in u_Action or "Back" in u_Action or "BACK" in u_Action:
            clear()
            dbMenu = False
        elif u_Action == "quit" or u_Action == "QUIT" or "Quit" in u_Action:
            clear()
            sys.exit()
        elif u_Action == "help" or u_Action == "HELP" or u_Action == "Help":
            clear()
            divider()
            print('Command Guide:\n\n'
                '(Key) Inv(.): Displays all keys tracked in inventory and their current inv. count. \n'
                '\nLow (stock keys): Use this to check which keys need to be resupplied. \n'
                '\n(Key) Stats: Use this to view various stats for each key. \n'
                '\nBack: Return to the previous menu. \n'
                '\nQuit: Close the program. Duh! \n')
            divider()
        else:
            clear()
            print('Input not valid.\n'
             'TIP: If you don''t know what to type, try entering, \"help\".')
            divider()