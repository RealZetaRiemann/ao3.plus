#! /usr/bin/python
""" Creates database for ao3graph.com """

# Running this file will create an empty database for ao3.plus

import sqlite3

# Create Database:

# open database
conn = sqlite3.connect('database.db')

# create tables
conn.execute('CREATE TABLE BAUTHORS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BFANDOMS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BRATINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BWARNINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCATEGORIES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOMPLETION (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BRELATIONSHIPS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCHARACTERS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BTAGS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BLANGUAGES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BWORDS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOLLECTIONS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BCOMMENTS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BKUDOS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BBOOKMARKS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BHITS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BDATESP (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE BDATESBM (username TEXT, col1 TEXT, UNIQUE(username))')

conn.execute('CREATE TABLE WGIFTEES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WFANDOMS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WRATINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WWARNINGS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WCATEGORIES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WCOMPLETION (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WRELATIONSHIPS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WCHARACTERS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WTAGS (username TEXT, keys TEXT, vals TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WLANGUAGES (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WWORDS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WCOLLECTIONS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WCOMMENTS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WKUDOS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WBOOKMARKS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WHITS (username TEXT, col1 TEXT, UNIQUE(username))')
conn.execute('CREATE TABLE WDATESP (username TEXT, col1 TEXT, UNIQUE(username))')

# close database
conn.close()
