#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/app/db.sqlite3')
curs = conn.cursor()

curs.execute('INSERT INTO memo_user VALUES("admin", "password")')
conn.commit()
curs.execute('INSERT INTO admin_admin VALUES("admin")')
conn.commit()
conn.close()