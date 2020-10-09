from django.urls import path

from memo.views import page_memo_list
from memo.views import page_login
from memo.views import page_logout
from memo.views import page_memo_view
from memo.views import page_report


urlpatterns = [
    path('memos', page_memo_list, name='memos'),
    path('login', page_login, name='login'),
    path('logout', page_logout, name='logout'),
    path('view/<int:idx>', page_memo_view, name='view'),
    path('report', page_report, name='report'),
]