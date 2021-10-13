from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .forms import RegistrationForm, LoginForm

from django.db.models import Q

from django.contrib.auth import authenticate, login, logout as django_logout
from django.core.paginator import Paginator
from django.core.validators import ValidationError

import base64

def login_user(request):
    params = {
        'login_form': LoginForm(),
    }
    if request.method == 'POST':
        params['login_form'] = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        username = request.POST['username']
        password = request.POST['password']
        username2 = base64.b64encode(username.encode())
        password2 = base64.b64encode(password.encode())
        if user is not None:
            login(request, user)
            return redirect('index', username=username2, password=password2)
        else:
            params['login_form'].add_error(None, "ユーザ名またはパスワードが異なります")
            return render(request, 'app/login.html', params)
    return render(request, 'app/login.html', params)
    #アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    #アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する

def registration_user(request):
    params = {
        'registration_form': RegistrationForm(),
    }
    if request.method == 'POST':
        params['registration_form'] = RegistrationForm(request.POST)
        if request.POST['email'].rsplit('@',1)[1] != 's.tsukuba.ac.jp' and request.POST['email'].rsplit('@',1)[1] != 'alumuni.tsukuba.ac.jp':
            params['registration_form'].add_error('email', "筑波大学のemailアカウントを使用してください。\n\n使用できるメールアドレス: sアド, alumuni")
        if params['registration_form'].has_error('email'):
            return render(request, 'app/registration.html', params)
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        return redirect('login')
    return render(request, 'app/registration.html', params)

def index(request, username, password):
    username_index = username.split("'")
    username = username_index[1]
    username3 = base64.b64decode(username).decode()

    password_index = password.split("'")
    password = password_index[1]
    password3 = base64.b64decode(password).decode()

    user = authenticate(username=username3, password=password3)
    if user is None:
        return redirect('login')
    return render(request, 'app/index.html')

def logout(request):
    django_logout(request)
    return render(request, 'studentdatabase/logout.html')