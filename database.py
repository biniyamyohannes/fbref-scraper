### database.py
### Functions that are accessing and modifying the database.

import pymysql

#Goes over the dictionary keys and creates the columns of the database table
def createInfoTable(header):
    #Connect to MySql
    try:
        conn = pymysql.connect(host='localhost',
        user='root', passwd='', db='SoccerStats')
        cur = conn.cursor()
    except:
        print("database: createTable: Exception was raised when trying to establish a connection to mysql.")

    #Create table
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS info (id VARCHAR(8) NOT NULL, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id));')
    except:
        print("database: createTable: Exception was raised when trying to create a table.")

    #Add columns
    for key in header:
        if type(key) is int:
            try:
                cur.execute('ALTER TABLE info ADD COLUMN %s INT;' %(key))
            except:
                print("database: createTable: Exception was raised when trying to add a column")
        else:
            try:
                cur.execute('ALTER TABLE info ADD COLUMN %s VARCHAR(50);' %(key))
            except:
                print("database: createTable: Exception was raised when trying to add a column")

    #Close Connection
    try:
        conn.close()
        cur.close()
    except:
        print("database: createTable: Exception was raised when trying to close the connection/cursor.")


def createStatsTables(tables):
    #Connect to MySql
    try:
        conn = pymysql.connect(host='localhost',
        user='root', passwd='', db='SoccerStats')
        cur = conn.cursor()
    except:
        print("database: createTable: Exception was raised when trying to establish a connection to mysql.")

    #Create tables
    for table in tables:
        try:
            cur.execute('CREATE TABLE IF NOT EXISTS %s (id VARCHAR(8) NOT NULL, FOREIGN KEY(id) REFERENCES info(id));' %(table[0]))
        except:
            print("database: createStatsTable: Exception was raised when trying to create a table.")
        
        #Add columns for each table
        for column in range(1, len(table)):
            try:
                cur.execute('ALTER TABLE %s ADD COLUMN %s FLOAT;' %(table[0], table[column]))
            except:
                print("database: createStatsTable: Exception was raised when trying to add a column")
                pass

#Add info to database
def addInfo(info):

	#Connect to MySQL database
    try:
        conn = pymysql.connect(host='localhost',
        user='root', passwd='', db='SoccerStats')
        cur = conn.cursor()
    except:
        print("database: addInfo: Exception was raised when trying to establish a connection to mysql.")

	#Add data
    for key in info:
        if key == 'id':
            try:
                cur.execute("INSERT INTO info (%s) VALUES ('%s');" % (key, info[key]))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to insert primary key (id).")
        else:
            try:
                print('UPDATE infi SET {0} = "{1}" WHERE id = "{2}";' .format(key, info[key], info['id']))
                cur.execute('UPDATE info SET {0} = "{1}" WHERE id = "{2}";' .format(key, info[key], info['id']))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to update a column.")
	
	#Close Connection
    try:
        conn.close()
        cur.close()
    except:
        print("database: addInfo: Exception was raised when trying to close the connection/cursor.")

def addStats(stats):

    #Connect to MySQL database
    try:
        conn = pymysql.connect(host='localhost',
            user='root',
            passwd='',
            db='SoccerStats')
        cur = conn.cursor()
    except:
        print("databaseL addStats: Exception was raised when trying to establish a connection to mysql.")

    #Add data
    for key in stats:
        if key == 'id':
            try:
                cur.execute("INSERT INTO stats (%s) VALUES ('%s');" % (key, stats[key]))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to insert primary key (id).")
        else:
            try:
                print('UPDATE stats SET {0} = "{1}" WHERE id = "{2}";' .format(key, stats[key], info['id']))
                 #try:
                cur.execute('UPDATE stats SET {0} = "{1}" WHERE id = "{2}";' .format(key, stats[key], stats['id']))
                cur.connection.commit()
            except:
                print("database: addInfo: Exception was raised when trying to update a column.")
    
    #Close Connection
    try:
        conn.close()
        cur.close()
    except:
        print("database: addInfo: Exception was raised when trying to close the connection/cursor.")
