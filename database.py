### database.py
### Functions that are accessing and modifying the database.

import pymysql

#Goes over the dictionary keys and creates the columns of the database table
def createTable(header):
    #Connect to MySql
    try:
        conn = pymysql.connect(host='localhost',
        user='root', passwd='Jolaus2333', db='SoccerStats')
        cur = conn.cursor()
    except:
        print("database: createTable: Exception was raised when trying to establish a connection to mysql.")

	#Create table
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS stats (id VARCHAR(8) NOT NULL, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id));')
    except:
        print("database: createTable: Exception was raised when trying to create a table.")

    #Add columns
    for key in header:
        if type(key) is int:
            try:
                cur.execute('ALTER TABLE stats ADD COLUMN %s INT;' %(key))
            except:
                print("database: createTable: Exception was raised when trying to add a column")
        else:
            try:
                cur.execute('ALTER TABLE stats ADD COLUMN %s VARCHAR(50);' %(key))
            except:
                print("database: createTable: Exception was raised when trying to add a column")


	#Close Connection
    try:
        conn.close()
        cur.close()
    except:
        print("database: createTable: Exception was raised when trying to close the connection/cursor.")


#Add info to database
def addInfo(info):

	#Connect to MySql
    try:
        conn = pymysql.connect(host='localhost',
        user='root', passwd='Jolaus2333', db='SoccerStats')
        cur = conn.cursor()
    except:
        print("database: addInfo: Exception was raised when trying to establish a connection to mysql.")

	#Add data
    for key in info:
        if key == 'id':
            try:
                cur.execute("INSERT INTO stats (%s) VALUES ('%s');" % (key, info[key]))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to insert primary key (id).")
        else:
            try:
                print('UPDATE stats SET {0} = "{1}" WHERE id = "{2}";' .format(key, info[key], info['id']))
			     #try:
                cur.execute('UPDATE stats SET {0} = "{1}" WHERE id = "{2}";' .format(key, info[key], info['id']))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to update a column.")
	
	#Close Connection
    try:
        conn.close()
        cur.close()
    except:
        print("database: addInfo: Exception was raised when trying to close the connection/cursor.")