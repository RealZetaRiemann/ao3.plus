""" Helper functions to update and retrieve information from the ao3graph.com database """
import sqlite3

def list_to_table(user, data, table):
    """ Updates table information, accepts a username, list of data, and table name as arguments """
    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user})

    count = 1
    column_title = 'col1'

    cursor.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = cursor.fetchone()

    for i in data:
        # add item to row
        cursor.execute("UPDATE {0} SET {1} = :new_value WHERE username=:user".format(table,column_title),
        {'new_value': i, 'user': user})
        if count != len(data):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                # add new column to table
                cursor.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))

    conn.commit()
    conn.close()

def dict_to_table(user, data, table):
    """ Updates table information, accepts a username, dictionary, and table name as arguments """
    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    user1 = user + " KEYS"
    keys = data.keys()

    cursor.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user1})

    count = 1
    column_title = 'col1'

    cursor.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = cursor.fetchone()
    
    for i in keys:
        # add item to row
        cursor.execute("UPDATE {0} SET {1} = :new_value WHERE username=:name".format(table,column_title), {'new_value': i, 'name': user1})
        if count != len(keys):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                # add new column to table
                cursor.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))

    user2 = user + " VALUES"
    values = data.values()

    cursor.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user2})

    count = 1
    column_title = 'col1'

    cursor.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = cursor.fetchone()
    
    for i in values:
        cursor.execute("UPDATE {0} SET {1} = :new_value WHERE username=:name".format(table,column_title), {'new_value': i, 'name': user2})   # add item to row
        if count != len(values):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                cursor.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))   # add new column to table

    conn.commit()
    conn.close()

def table_to_dict(user, table):
    """ Returns dictionary of data from table and takes a username and table name as parameters """

    newdict = {}

    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    userk = user + " KEYS"
    userv = user + " VALUES"

    keys = cursor.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': userk})
    keys = cursor.fetchone()
    vals = cursor.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': userv})
    vals = cursor.fetchone()
    count = 1

    for key in keys:
        if key is None:
            break
        if key != user + " KEYS":
            newdict[key] = int(vals[count])
            count += 1

    return newdict

def table_to_list(user, table):
    """ Returns list of data from table and takes a username and table name as parameters """

    newlist = []

    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    items = cursor.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': user})
    items = cursor.fetchone()
    count = 0

    for item in items:
        if item is None:
            break
        if item != user:
            newlist.append(item)
            count += 1

    return newlist

def dict_to_TAGtable(user, data, table):
    """ Updates table information, accepts a username, dictionary, and table name as arguments """
    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    keystring = ""
    keys = data.keys()

    cursor.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user})
    
    for key in keys:
        keystring = keystring + str(key) + ","

    cursor.execute("UPDATE {0} SET keys = :new_value WHERE username=:name".format(table), {'new_value': keystring, 'name': user})

    valuestring = ""
    values = data.values()
    
    for val in values:
        valuestring = valuestring + str(val) + ","

    cursor.execute("UPDATE {0} SET vals = :new_value WHERE username=:name".format(table), {'new_value': valuestring, 'name': user})

    conn.commit()
    conn.close()

def TAGtable_to_dict(user, table):
    """ Returns dictionary of data from table and takes a username and table name as parameters """

    newdict = {}

    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    cursor = conn.cursor()

    keys = cursor.execute("SELECT keys FROM {} WHERE username = (:name)".format(table), {'name': user})
    keys = cursor.fetchone()
    vals = cursor.execute("SELECT vals FROM {} WHERE username = (:name)".format(table), {'name': user})
    vals = cursor.fetchone()
    count = 0

    keys = keys[0].split(",")
    vals = vals[0].split(",")

    for key in keys:
        if key is not "":
            newdict[key] = int(vals[count])
            count += 1

    return newdict