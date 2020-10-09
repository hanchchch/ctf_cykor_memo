#!/usr/bin/env python3
import time
import sqlite3

import requests

conn = sqlite3.connect('/app/db.sqlite3')
SLEEP_TIME = 2
length = 0

def main():
    run_loop()

def check_report():
    curs = conn.cursor()
    curs.execute('SELECT * FROM admin_report')
    reports = curs.fetchall()
    curs.close()
    if length != len(reports):
        length = len(reports)
        return reports[length-1][1]
    else:
        return False
    
def visit(url):
    res = requests.get(url, headers={
        "User-Agent": "Cykor memo admin",
        "Cookie": "admin_cookie"
    }, timeout=1)
    print(res.text)

def run_loop():
    while True:
        try:
            url = check_report()
            if url:
                visit(url)
        except Exception:
            pass
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
