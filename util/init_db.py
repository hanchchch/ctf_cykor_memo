#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/app/db.sqlite3')
curs = conn.cursor()

curs.execute('INSERT INTO memo_user VALUES("admin", "02f09d5c4c3f2bc0d0e5ec7147de88e7e3c3651eee99cca0554be24718fc492f")')
conn.commit()
curs.execute('INSERT INTO admin_admin VALUES("admin")')
conn.commit()
conn.close()