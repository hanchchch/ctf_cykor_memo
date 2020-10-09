import hashlib
import jwt
import time

from django import forms

from memo.models import Memo, User

from cykor_memo.settings import SECRET_KEY, SESSION_TIME
from cykor_memo.common import check_safeline, db, sha256, SUCCESS

class MemoForm(forms.Form):
    title = forms.CharField(max_length=30)
    content = forms.CharField(max_length=100)
    # TODO filtering

def new_memo(title, content, username):
    if check_safeline(title) is False:
        return '^([a-z]|[0-9])+$'
    if check_safeline(content) is False:
        return '^([a-z]|[0-9])+$'
    name = db.get(User, {'name':username})
    idx = len(get_memo_list(username))
    db.insert(Memo, {'index':idx, 'title':title, 'content':content, 'name':name})
    return SUCCESS

def get_memo_list(username):
    memos = db.get_all(Memo, {'name':username})
    memo_list = []
    for memo in memos:
        memo_list.append({'title':memo.title, 'idx':memo.index})
    return memo_list

def get_memo(idx, username):
    memo = db.get(Memo, {'index':idx,'name':username})
    return {'title':memo.title, 'content':memo.content, 'author':memo.name.name}