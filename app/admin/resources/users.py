from django import forms

from admin.models import Admin
from memo.models import User
from yonsei_memo.common import db
from yonsei_memo.common import SUCCESS


def isAdmin(username):
    res = db.get(Admin, {'name':username})
    if res is not None:
        return True
    return False

def get_user_list(filters):
    users = db.get_all(User, filters, 'name')
    user_list = []
    for user in users:
        user_list.append({'name':user.name})
    return user_list
