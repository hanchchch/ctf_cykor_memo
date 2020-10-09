from django.shortcuts import redirect

from memo.models import User, Memo

from memo.resources.user import get_user, get_token, register_user, LoginForm
from memo.resources.memo import get_memo_list, get_memo, new_memo, MemoForm
from memo.resources.report import ReportForm, new_report
from cykor_memo.common import SUCCESS, temp_memo_login, temp_memo_memo, temp_memo_memolist, temp_memo_report, render_template

def page_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if request.POST.get('register') is not None:
                res = register_user(username, password)
                if res == SUCCESS:
                    token = get_token(username, password)
                    response = redirect('memos')
                    response.set_cookie('token', token, httponly=True)
                    return response
                else:
                    msg = res

            elif request.POST.get('login') is not None:
                token = get_token(username, password)
                if token is not None:
                    response = redirect('memos')
                    response.set_cookie('token', token, httponly=True)
                    return response
                else:
                    msg = 'Wrong username or password.'     

            else:
                msg = 'Wrong form.' 
            
            return render_template(temp_memo_login, {'msg':msg,'form': form})
        
        return render_template(temp_memo_login, {'msg':'Wrong form.','form': form})
    else:
        username = get_user(request)
        if username is not None:
            return redirect('memos')
        form = LoginForm()
        return render_template(temp_memo_login, {'form': form})

def page_logout(request):
    response = redirect('login')
    response.set_cookie('token', '', httponly=True)
    return response

def page_memo_list(request):
    username = get_user(request)
    if username is None:
        return redirect('login')

    msg = None
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            res = new_memo(title, content, username)
            if res == SUCCESS:
                return redirect('memos')
            else:
                msg = res

    memo_list = get_memo_list(username)
    context = {'memo_list': memo_list, 'form':MemoForm, "msg":msg}
    return render_template(temp_memo_memolist, context)


def page_memo_view(request, idx):
    username = get_user(request)
    if username is None:
        return redirect('login')

    memo = get_memo(idx, username)
    return render_template(temp_memo_memo, {"memo":memo})

def page_report(request):
    username = get_user(request)
    if username is None:
        return redirect('login')

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url')
            res = new_report(url, username)
            if res == SUCCESS:
                msg = 'Thanks!'
            else:
                msg = res
        else:
            msg = 'Wrong form.' 
                    
        return render_template(temp_memo_report, {'msg':msg,'form':form})
    else:
        form = ReportForm()
        return render_template(temp_memo_report, {'form':form})
