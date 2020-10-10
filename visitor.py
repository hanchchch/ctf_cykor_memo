#!/usr/bin/env python3
import time
import sqlite3

import requests

conn = sqlite3.connect('/app/db.sqlite3')
curs = conn.cursor()
SLEEP_TIME = 1

def main(token):
    run_loop(token)

def check_report(length):
    curs.execute('SELECT * FROM admin_report')
    reports = curs.fetchall()
    if length != len(reports):
        length += 1
        return [reports[length-1][1], length]
    else:
        return False
    
def visit(url, token):
    requests.get(url, headers={
        "User-Agent": "admin"
    }, cookies={'token':token}, timeout=0.1)

def run_loop(token):
    length = 0
    while True:
        try:
            url = check_report(length)
            if url:
                visit(url[0], token)
                length = url[1]
        except Exception:
            pass
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    url = 'http://127.0.0.1:8080'
    reg_form = {"username":"admin", "password":"5uP3R_DuP3R_53CR37_p4ssvv0ord_h4nch_!@#!@#_12341234_", "login":"Login"}
    res = requests.post(url+'/memo/login', data=reg_form)
    token = res.history[0].cookies['token']

    main(token)
