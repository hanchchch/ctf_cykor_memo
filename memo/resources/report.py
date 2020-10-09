from django import forms

from admin.models import Report
from memo.models import User
from cykor_memo.common import db,  SUCCESS, check_url

class ReportForm(forms.Form):
    url = forms.CharField(max_length=30)
    # TODO filtering

def new_report(url, username):
    if check_url(url) is False:
        return 'invalid url.'
    name = db.get(User, {'name':username})
    idx = len(get_report_list())
    db.insert(Report, {"index":idx, "url":url, "name":name})
    return SUCCESS

def get_report_list():
    reports = db.get_all(Report)
    report_list = []
    for report in reports:
        report_list.append({'idx':report.index, 'url':report.url, 'user':report.name})
    return report_list
