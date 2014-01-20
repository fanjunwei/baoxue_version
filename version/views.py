# coding=utf-8
# Create your views here.
import django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login as auth_login
from django.shortcuts import render_to_response
from tools import *
from models import *
from django.db.models import Q

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

def test(request):
    return render_to_response('test.html')

def manageBranch(request):
    return render_to_response('manageBranch.html')

def saveBranch(request):
    if request.method == "POST":
        name=request.POST.get('name')
        if not name:
            return getResult(False,'分支名不能为空')
        description=request.POST.get('description')
        try:
            branch=Branch()
            branch.name=name
            branch.description=description
            branch.save()
            return getResult(True)
        except django.db.utils.IntegrityError:
            return getResult(False,'该分支已存在')
        except Exception,e:
            return getResult(False,str(e))

def getBranches(request):
    keyword=request.POST.get('keyword','')
    branches=Branch.objects.filter(Q(name__icontains=keyword)|Q(description__icontains=keyword))
    result=[]
    for b in branches:
        item=[b.id,b.name,b.description]
        result.append(item)
    return getResult(True,result=result)

def delBranches(request):
    id=request.POST.get('id')
    if id:
        try:
            branch=Branch.objects.get(id=id)
            if branch:
                branch.delete()
                return getResult(True)
        except Exception,e:
            return getResult(False,str(e))
    return getResult(False,'删除失败')
