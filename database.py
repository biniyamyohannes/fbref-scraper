# database.py
"""Functions that are accessing and modifying the database."""

from typing import List, Dict

import pymysql


def connect_to_db():
    """
    Establish a connection with the database.

    Returns:
        conn -- pymysql connection object
        cur -- database cursor for the current connection
    """
    try:
        conn = pymysql.connect(host='localhost',
                               user='root', passwd='', db='SoccerStats')
        cur = conn.cursor()
        return conn, cur

    except:
        print("database: connect_to_db: "
              "Exception was raised when trying to establish a connection to mysql.")


def close_db_connection(conn, cur) -> None:
    """
    Close the database connection and the database cursor.

    Arguments:
        conn -- pymysql database connection object
        cur -- database cursor object
    """
    try:
        conn.close()
        cur.close()
    except:
        print("database: close_db_connection: "
              "Exception was raised when trying to close the connection/cursor.")


def create_info_table() -> None:
    """
    Create a database table to hold general information about a player.
    This db table is created separately from the stats tables because
    this information is not in a html table like the other stats.
    """
    header = {'name': '', 'position': '', 'foot': '', 'height': 0, 'weight': 0, 'dob': '',
              'cityob': '', 'countryob': '', 'nt': '', 'club': '', 'age': 0}

    conn, cur = connect_to_db()

    try:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS '
            'info (id VARCHAR(8) NOT NULL, '
            'created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, '
            'PRIMARY KEY(id));')
    except:
        print("database: create_info_table: Exception was raised when trying to create a table.")

    # Add columns
    for col in header:

        # Add columns with int type
        if isinstance(header[col], int):
            try:
                cur.execute(f'ALTER TABLE info ADD COLUMN {col} INT;')
            except:
                print("database: create_info_table: "
                      "Exception was raised when trying to add a column")

        # Add columns with string type
        else:
            try:
                cur.execute(f'ALTER TABLE info ADD COLUMN {col} VARCHAR(50);')
            except:
                print("database: create_info_table: "
                      "Exception was raised when trying to add a column")

    close_db_connection(conn, cur)


def create_stats_tables(tables: List[List[str]]) -> None:
    """
    Create the stats tables if they don't exist.

    Arguments:
        tables -- a list of string lists,
               -- table[i][0] is the name of the i-th table
               -- table [i][1:] are the column names for the table
    """
    conn, cur = connect_to_db()

    # Create tables
    for table in tables:
        try:
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {table[0]} (id VARCHAR(8) NOT NULL, '
                f'PRIMARY KEY(id), FOREIGN KEY(id) REFERENCES info(id));')
        except:
            print("database: create_stats_table: "
                  "Exception was raised when trying to create a table.")

        # Add columns for each table
        for column in range(1, len(table)):
            try:
                cur.execute(f'ALTER TABLE {table[0]} ADD COLUMN {table[column]} FLOAT;')
            except:
                print("database: createStatsTable: "
                      "Exception was raised when trying to add a column")

    close_db_connection(conn, cur)


def add_info(info: Dict) -> None:
    """
    Inserts the general information about a player (name, age, position, etc.) into
    the info table.

    Arguments:
        info -- A dictionary with column names as keys and player information as values.
             -- for example {'name':'Thibaut Courtois', 'position':'GK', ..., 'age':29}
    """
    conn, cur = connect_to_db()

    # Add data into the info table
    for key in info:

        # Insert primary key
        if key == 'id':
            try:
                cur.execute(f"INSERT INTO info ({key}) "
                            f"VALUES ('{info[key]}');")
                cur.connection.commit()
            except:
                print("database: add_info: "
                      "Exception was raised when trying to insert primary key (id).")

        # Insert data
        else:
            try:
                cur.execute(f'UPDATE info '
                            f'SET {key} = "{info[key]}" W'
                            f'HERE id = "{info["id"]}";')
                print(f'UPDATE info '
                      f'SET {key} = "{info[key]}" '
                      f'WHERE id = "{info["id"]}";')
                cur.connection.commit()
            except:
                print("database: add_info: Exception was raised when trying to update a column.")

    close_db_connection(conn, cur)


def add_stats(stats: List[Dict]) -> None:
    """
    Insert player performance data into the appropriate table.

    Arguments:
        stats -- list of dictionaries
              -- each dictionary represents a different table (shooting, passing, etc.)
    """
    conn, cur = connect_to_db()

    # Iterate over the dictionaries each of which represents one table
    for table in stats:

        # Iterate over the dict keys each of which represents a table's columns
        for column in table:

            # Skip the table name
            if column == 'table':
                pass

            # Insert the id value (primary key)
            elif column == 'id':
                try:
                    cur.execute(f'REPLACE INTO {table["table"]} ("id") '
                                f'VALUES ("{table["id"]}");')
                    cur.connection.commit()
                except:
                    print("database: add_stats: "
                          "Exception was raised when trying to insert primary key (id).")

            # Insert data into appropriate columns
            else:
                try:
                    cur.execute(
                        f'UPDATE {table["table"]} '
                        f'SET {column} = {table[column]} '
                        f'WHERE id = "{table["id"]}";')
                    print(
                        f'UPDATE {table["table"]} '
                        f'SET {column} = {table[column]} '
                        f'WHERE id = "{table["id"]}";')
                    cur.connection.commit()
                except:
                    print("database: add_stats: "
                          "Exception was raised when trying to update a column.")

    close_db_connection(conn, cur)
