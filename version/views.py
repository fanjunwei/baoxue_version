# coding=utf-8
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login as auth_login
from django.shortcuts import render_to_response
from tools import *


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return getResult(True)
        else:
            return getResult(False,'用户名或密码错误')
    else:
        return render_to_response('login.html')

@login_required
def main(request):
    return render_to_response('main.html')
