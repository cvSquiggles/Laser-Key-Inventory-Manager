# Laser Key Inventory Script System
This is a tool I created to automate the management of the laser coated key inventory at Depco Products Inc.

## Prerequisites
pyodbc == 4.0.26
tabulate == 0.8.3

## Set-up
1. Populate a database with the *.mdf* in dbFiles.
2. Open the *utility.py* file in a text editor, and change the **DVNAME**, **DBNAME**, and **SVNAME** to your driver, database, and server name.
3. Start by running *keyInventoryScripts/laserKeyInv_exe.py* and follow prompts.  You can type help to get a list of commands.

## Use
The inital menu is used to handle daily activities such as filling orders, while the **Access Database** menu is for big picture managment,
with stats, and a tool to determine which keys need to be re-ordered soon.

### Author
Steven Alexander Jones
"I couldn't have done it without my homie, google."

### License
This project is licensed under the GNU General Public License v.3 - see *LICENSE.md* file for details.
