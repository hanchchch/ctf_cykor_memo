import hashlib
import re
from urllib.parse import urlparse

from django.template import Template, Context
from django.http import HttpResponse

from cykor_memo.settings import DOMAIN

SHA256_DIGEST_LEN = 64
SUCCESS = 'SUCCESS'

with open('templates/index.html') as temp:
    temp_index = temp.read()
with open('templates/admin/userlist.html') as temp:
    temp_admin_userlist = temp.read()
with open('templates/memo/login.html') as temp:
    temp_memo_login = temp.read()
with open('templates/memo/memolist.html') as temp:
    temp_memo_memolist = temp.read()
with open('templates/memo/memo.html') as temp:
    temp_memo_memo = temp.read()
with open('templates/memo/report.html') as temp:
    temp_memo_report = temp.read()

def render_template(template, context):
    page = temp_index.split('body_here')[0]
    page += template
    page += temp_index.split('body_here')[1]
    return HttpResponse(Template(page).render(Context(context)))

def check_safeline(string):
    regex = re.compile(r'^([a-z]|\d)+$')
    matchobj = regex.search(string)
    if matchobj is None:
        return False
    elif matchobj.group() != string:
        return False
    else:
        return True

def check_url(url):
    o = urlparse(url)
    if o.scheme != 'http':
        if o.scheme != 'https':
            return False
    if o.netloc != DOMAIN:
        return False
    return True

def sha256(s):
    if type(s) != bytes:
        if type(s) == str:
            s = s.encode('utf-8')
        else:
            return None
    return hashlib.sha256(s).hexdigest()

class DB:
    def get_all(self, model, filters={}, order_by='-index'):
        try:
            results = model.objects.all().filter(**filters).order_by(order_by)
        except model.DoesNotExist:
            return []
        return results
    
    def get(self, model, filters):
        try:
            result = model.objects.get(**filters)
        except model.DoesNotExist:
            return None
        return result

    def insert(self, model, args):
        abj = model(**args)
        abj.save()

db = DB()