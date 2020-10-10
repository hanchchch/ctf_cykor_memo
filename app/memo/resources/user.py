import jwt
import time

from django import forms

from memo.models import User

from cykor_memo.settings import SECRET_KEY
from cykor_memo.common import check_safeline, db, sha256, SUCCESS

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField()
    # TODO filtering

def register_user(username, password):
    if check_safeline(username) is False:
        return '^([a-z]|[0-9])+$'
    if db.get(User, {'name':username}) is None:
        db.insert(User, {'name':username, 'password':sha256(password)})
        return SUCCESS
    else:
        return 'Already exists.'

def get_token(username, password):
    user = db.get(User, {'name':username, 'password':sha256(password)})
    if user is None:
        return None
    else:
        return jwt.encode(
            {
                'username':user.name,
                'iat':round(time.time()),
            }, SECRET_KEY).decode('utf-8')

def get_user(request):
    if request.COOKIES.get('token') is not None:
        token = request.COOKIES.get('token')
        try:
            payload = jwt.decode(token, SECRET_KEY)
        except Exception:
            return None
        if payload.get('username') is not None:
            return payload.get('username')
    else:
        return None
