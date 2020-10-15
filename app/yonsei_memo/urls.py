from django.urls import path, include
from django.shortcuts import redirect

def to_login(request):
    return redirect('/memo/login')

urlpatterns = [
    path('', to_login),
    path('admin/', include('admin.urls')),
    path('memo/', include('memo.urls'))
]
