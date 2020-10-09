from django.urls import path

from admin.views import page_user_list

urlpatterns = [
    path('users', page_user_list, name='users'),
]