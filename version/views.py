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
import xml.sax.saxutils as saxutils

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

def manageSubBranch(request):
    return render_to_response('manageSubBranch.html')

def manageVersion(request):
    return render_to_response('manageVersion.html')

def saveBranch(request):
    if request.method == "POST":
        name=request.POST.get('name')
        id=request.POST.get('id')
        if not name:
            return getResult(False,'分支名不能为空')
        description=request.POST.get('description')
        try:
            if id:
                branches=Branch.objects.filter(id=id)
                if branches.count()==0:
                    return getResult(False,'分支错误，请重新选择')
                else:
                    branch=branches[0]
            else:
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
        item=[b.id,b.name,multilineHtml(b.description)]
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

def multilineHtml(raw):
    return saxutils.escape(raw).replace('\n','<br/>')


def searchBranchesName(request):
    term=request.REQUEST.get('term')
    if term :
        branches=Branch.objects.filter(name__icontains=term)
        result=[]
        for b in branches:
            item=b.name
            result.append(item)
        return getResult(True,result=result)
    else:
        return getResult(False)

def getSubBranches(request):
    keyword=request.POST.get('keyword','')
    subbranches=SubBranch.objects.filter(Q(name__icontains=keyword)|Q(branch__name__icontains=keyword)|Q(description__icontains=keyword)).order_by('branch','name')
    result=[]
    for b in subbranches:
        item=[b.id,b.branch.name,b.name,multilineHtml(b.description)]
        result.append(item)
    return getResult(True,result=result)

def saveSubBranch(request):
    if request.method == "POST":
        branchName=request.POST.get('branch')
        name=request.POST.get('name')
        id=request.POST.get('id')
        if not branchName:
            return getResult(False,'所属分支不能为空')

        if not name:
            return getResult(False,'子分支名不能为空')

        branches=Branch.objects.filter(name=branchName)
        if(branches.count()==0):
            branch=Branch()
            branch.name=branchName
            branch.save()
        else:
            branch=branches[0]
        description=request.POST.get('description')
        try:
            if id:
                subbranches=SubBranch.objects.filter(id=id)
                if subbranches.count()==0:
                    return getResult(False,'分支错误，请重新选择')
                else:
                    subbranch=subbranches[0]
            else:
                subbranch=SubBranch()
            subbranch.name=name
            subbranch.branch=branch
            subbranch.description=description
            subbranch.save()
            return getResult(True)
        except django.db.utils.IntegrityError:
            return getResult(False,'该子分支已存在')
        except Exception,e:
            return getResult(False,str(e))

def delSubBranches(request):

    id=request.POST.get('id')
    if id:
        try:
            subbranch=SubBranch.objects.get(id=id)
            subbranch.delete()
            return getResult(True)
        except Exception,e:
            return getResult(False,str(e))
    return getResult(False,'删除失败')


def getVersions(request):
    keyword=request.POST.get('keyword','')
    versions=Version.objects.filter(Q(fullName__icontains=keyword)|Q(description__icontains=keyword)).order_by('subBranch','name')
    result=[]
    for b in versions:
        item=[b.id,b.getFullName(),multilineHtml(b.description)]
        result.append(item)
    return getResult(True,result=result)