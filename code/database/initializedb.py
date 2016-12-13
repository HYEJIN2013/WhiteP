#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

def get_users():
    with open("createdusers.log") as f:
            users = []
            lines = f.readlines()
            for item in lines:
                item = item.strip()
                user = item.split(':')
                users.append(user)
            return users

def main():
    users = get_users()
    con = None
    try:
        con = lite.connect('db/tarbackup.db')
        with con:
           cur = con.cursor()   
           cur.execute("DROP TABLE IF EXISTS Users")
           cur.execute("CREATE TABLE Users("\
            "Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT, "\
            " Email TEXT, Created TEXT)")
           cur.execute("CREATE TABLE UsersToCreate("\
            "Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Password TEXT, "\
            "Email TEXT, Created TEXT)")
           cur.executemany("INSERT INTO Users("\
            "Name, Password, Email, Created) VALUES(?, ?, ?, CURRENT_TIMESTAMP)", 
           users)
          
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
        
    finally:
        if con:
            con.close()

main()
