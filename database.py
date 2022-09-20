# This file includes functions to update and retrieve information from the Ao3graph database
import sqlite3

# Updates table information and accepts a username, list of data, and table name as arguments
def list_to_table(user, data, table):
    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user})

    count = 1
    column_title = 'col1'

    c.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = c.fetchone()
    
    for i in data:
        c.execute("UPDATE {0} SET {1} = :new_value WHERE username=:user".format(table,column_title), {'new_value': i, 'user': user})    # add item to row
        if count != len(data):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                c.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))                                             # add new column to table

    conn.commit()
    conn.close()

# Updates table information and accepts a username, dictionary of data, and table name as arguments
def dict_to_table(user, data, table):
    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    c = conn.cursor()

    user1 = user + " KEYS"
    keys = data.keys()

    c.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user1})

    count = 1
    column_title = 'col1'

    c.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = c.fetchone()
    
    for i in keys:
        c.execute("UPDATE {0} SET {1} = :new_value WHERE username=:name".format(table,column_title), {'new_value': i, 'name': user1})   # add item to row
        if count != len(keys):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                c.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))                                             # add new column to table

    user2 = user + " VALUES"
    values = data.values()

    c.execute("INSERT OR IGNORE INTO {} (username) VALUES (:name)".format(table), {'name': user2})

    count = 1
    column_title = 'col1'

    c.execute("SELECT COUNT(*) FROM pragma_table_info('{}')".format(table))
    colcount = c.fetchone()
    
    for i in values:
        c.execute("UPDATE {0} SET {1} = :new_value WHERE username=:name".format(table,column_title), {'new_value': i, 'name': user2})   # add item to row
        if count != len(values):                                                                                                    
            count += 1
            column_title = 'col' + str(count)
            if count >= colcount[0]:
                c.execute("ALTER TABLE {0} ADD COLUMN {1} TEXT".format(table,column_title))                                             # add new column to table

    conn.commit()
    conn.close()

# Returns dictionary of data from table and takes a username and table name as parameters
def table_to_dict(user, table):

    dict = {}

    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    c = conn.cursor()

    userk = user + " KEYS"
    userv = user + " VALUES"

    keys = c.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': userk})
    keys = c.fetchone()
    vals = c.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': userv})
    vals = c.fetchone()
    count = 1

    for key in keys:
        if key == None:
            break
        if key != user + " KEYS":
            dict[key] = int(vals[count])
            count += 1
    
    return dict

# Returns list of data from table and takes a username and table name as parameters
def table_to_list(user, table):

    list = []

    conn = sqlite3.connect("/home/ronia/ao3graph/db/database.db")
    c = conn.cursor()

    items = c.execute("SELECT * FROM {} WHERE username = (:name)".format(table), {'name': user})
    items = c.fetchone()
    count = 0

    for item in items:
        if item == None:
            break
        if item != user:
            list.append(item)
            count += 1

    return list
