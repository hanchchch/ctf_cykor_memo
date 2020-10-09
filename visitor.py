#!/usr/bin/env python3
import time
import sqlite3

import requests

conn = sqlite3.connect('/app/db.sqlite3')
curs = conn.cursor()
SLEEP_TIME = 0.2

def main():
    run_loop()

def check_report(length):
    curs.execute('SELECT * FROM admin_report')
    reports = curs.fetchall()
    if length != len(reports):
        length = len(reports)
        return [reports[length-1][1], length]
    else:
        return False
    
def visit(url):
    res = requests.get(url, headers={
        "User-Agent": "Cykor memo admin",
        "Cookie": "admin_cookie"
    }, timeout=1)
    print(res.text)

def run_loop():
    length = 0
    while True:
        try:
            print('check')
            url = check_report(length)
            if url:
                visit(url[0])
                length = url[1]
        except Exception:
            pass
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
