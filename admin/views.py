from django.shortcuts import redirect

from cykor_memo.common import SUCCESS, temp_admin_userlist, render_template

from memo.resources.user import get_user
from admin.resources.users import get_user_list, isAdmin

def page_user_list(request):
    username = get_user(request)
    if username is None:
        return redirect('memos')

    if not isAdmin(username):
        return redirect('memos')
    
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
