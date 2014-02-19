# coding=utf-8
# Create your views here.
import datetime
import time
import django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login as auth_login
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import re
from tools import *
from models import *
from django.db.models import Q
from django.core.cache import cache
import xml.sax.saxutils as saxutils
from version.db_view import *


def login(request):
    if User.objects.all().count()==0:
        user = User()
        user.username = 'SW'
        user.set_password('SW')
        user.save()
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
@login_required
def test(request):
    return render_to_response('test.html')
@login_required
def manageBranch(request):
    return render_to_response('manageBranch.html')
@login_required
def manageSubBranch(request):
    return render_to_response('manageSubBranch.html')

@login_required
def manageVersion(request):
    return render_to_response('manageVersion.html')

def browseVersion(request):
    manage=request.REQUEST.get('manage')
    if not manage=='1':
        hasManage=True
    else:
        hasManage=False
    return render_to_response('browseVersion.html',{'hasManage':hasManage})

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
        item=[b.id,b.branch.name,b.name,b.description]
        result.append(item)
    return getResult(True,result=result)

def saveSubBranch(request):
    if request.method == "POST":
        branchName=request.POST.get('branch')
        name=request.POST.get('name')
        id=request.POST.get('id')
        if not branchName:
            return getResult(False,'所属分支不能为空')

        branches=Branch.objects.filter(name=branchName)
        if(branches.count()==0):
            # branch=Branch()
            # branch.name=branchName
            # branch.save()
            return getResult(False,'所属分支不存在')
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
    versions=Version.objects.filter(Q(fullName__icontains=keyword)|Q(parentFullName__icontains=keyword)|Q(description__icontains=keyword)).order_by('subBranch','createTime')
    result=[]
    for b in versions:
        baseVersionFullName=''
        if b.parent:
            baseVersions=Version.objects.filter(id=b.parent)
            if baseVersions.count()>0:
                baseVersionFullName=baseVersions[0].getFullName()

        #item=[b.id,b.getFullName(),baseVersionFullName,b.description]
        item={
            'id':b.id,
            'branch':b.subBranch.branch.name,
            'subBranch':b.subBranch.name,
            'name':b.name,
            'fullName':b.getFullName(),
            'parentFullName':baseVersionFullName,
            'desc':b.description,

        }
        result.append(item)
    return getResult(True,result=result)


def searchSubBranchesName(request):
    branch=request.REQUEST.get('branch')
    term=request.REQUEST.get('term')
    subbranches=SubBranch.objects.filter(Q(name__icontains=term)&Q(branch__name=branch))
    result=[]
    for b in subbranches:
        item=b.name
        result.append(item)
    return getResult(True,result=result)


def searchVersionFullName(request):
    term=request.REQUEST.get('term')
    if term :
        versions=Version.objects.filter(fullName__icontains=term)
        result=[]
        for b in versions:
            item=b.fullName
            result.append(item)
        return getResult(True,result=result)
    else:
        return getResult(False)


def getAutoBaseVersionName(request):
    if request.method == "POST":
        branchName=request.POST.get('branch')
        subbranchName=request.POST.get('subbranch')
        if not branchName:
            return getResult(False,'所属分支不能为空')
        if not subbranchName:
            return getResult(False,'所属子分支不能为空')
        branches=Branch.objects.filter(name=branchName)
        if(branches.count()>0):
            branch=branches[0]
            subbranches=SubBranch.objects.filter(branch=branch,name=subbranchName)
            if subbranches.count()>0:
                subbranch=subbranches[0]
                versions=Version.objects.filter(subBranch=subbranch).order_by('-createTime')
                if versions.count()>0:
                    return getResult(True,result=versions[0].fullName)
    return getResult(False)



def saveVersion(request):
    if request.method == "POST":
        branchName=request.POST.get('branch')
        subbranchName=request.POST.get('subbranch')
        baseVersionFullName=request.POST.get('baseversion')
        name=request.POST.get('name')
        id=request.POST.get('id')
        if not branchName:
            return getResult(False,'所属分支不能为空')

        # if not subbranchName:
        #     return getResult(False,'所属子分支不能为空')

        if not name:
            return getResult(False,'版本号不能为空')



        branches=Branch.objects.filter(name=branchName)
        if(branches.count()==0):
            # branch=Branch()
            # branch.name=branchName
            # branch.save()
            # subbranch=SubBranch()
            # subbranch.name=subbranchName
            # subbranch.branch=branch
            # subbranch.save()
            return getResult(False,'所属分支不存在')
        else:
            branch=branches[0]
            subbranches=SubBranch.objects.filter(branch=branch,name=subbranchName)
            if subbranches.count()==0:
                subbranch=SubBranch()
                subbranch.name=subbranchName
                subbranch.branch=branch
                subbranch.save()
            else:
                subbranch=subbranches[0]

        description=request.POST.get('description')
        try:
            if id:
                isAddVersion=False
                versions=Version.objects.filter(id=id)
                if versions.count()==0:
                    return getResult(False,'版本号错误，请重新选择')
                else:
                    version=versions[0]
            else:
                isAddVersion=True
                version=Version()
            if not isAddVersion:
                oldFullVersion=version.getFullName()
            version.name=name
            version.subBranch=subbranch
            version.description=description
            if baseVersionFullName:
                baseVersions=Version.objects.filter(fullName=baseVersionFullName)
                if baseVersions.count()>0:
                    version.parent=baseVersions[0].id
                    version.parentFullName=baseVersions[0].getFullName()
                else:
                    return getResult(False,'基于版本不存在')
            version.save()
            if not isAddVersion:
                if not oldFullVersion == version.getFullName():
                    isAddVersion=True
            if isAddVersion:
                sub=u'版本记录:'+version.getFullName()
                content=version.getFullName()+'\n'
                if version.parentFullName :
                    content=content+u'基于版本:'+version.parentFullName+'\n'
                content=content+u'===============================================\n'
                content=content+version.description+'\n'
                content=content+u'===============================================\n'
                content=content+u'由服务器自动发送，请勿回复此邮件\n'
                sub=sub.encode('utf8')
                content=content.encode('utf8')
                send_mail(settings.MAIL_TO,sub,content)
            return getResult(True)
        except django.db.utils.IntegrityError:
            return getResult(False,'该版本已存在')
        except Exception,e:
            return getResult(False,str(e))

def delVersion(request):

    id=request.POST.get('id')
    if id:
        try:
            version=Version.objects.get(id=id)
            version.delete()
            return getResult(True)
        except Exception,e:
            return getResult(False,str(e))
    return getResult(False,'删除失败')

def getVersionFullNameFromID(id):
    if id:
        baseVersions=Version.objects.filter(id=id)
        if baseVersions.count()>0:
            return baseVersions[0].fullName

    return ''

def getVersionForBrowse(request):
    keyword=request.POST.get('keyword','')
    today=(request.POST.get('today','').lower()=='true')
    start= datetime.date.today()
    if today:
        versions_all=Version.objects.filter(Q(createTime__gt=start)&(Q(fullName__icontains=keyword)|Q(parentFullName__icontains=keyword)|Q(description__icontains=keyword))).order_by('subBranch__branch','subBranch','createTime')
    else:
        versions_all=Version.objects.filter(Q(fullName__icontains=keyword)|Q(parentFullName__icontains=keyword)|Q(description__icontains=keyword)).order_by('subBranch__branch','subBranch','createTime')
    result=[]
    paginator=Paginator(versions_all,50)
    try:
        p=int(request.REQUEST.get('p','1'))
    except ValueError:
        p=1
    try:
        versions=paginator.page(p)
    except (EmptyPage, InvalidPage):
        p=paginator.num_pages
        versions=paginator.page(paginator.num_pages)

    for b in versions:
        item={
            'branch_name':b.subBranch.branch.name,
            'branch_desc':b.subBranch.branch.description,
            'subbranch_name':b.subBranch.getFullName(),
            'subbranch_desc':b.subBranch.description,
            'version_fullname':b.fullName,
            'version_base':getVersionFullNameFromID(b.parent),
            'version_desc':b.description,
        }
        url=getDownloadUrl(b.getFullName())
        if url :
            item['url']=url
            item['has_url']=True
        else:
            item['has_url']=False

        result.append(item)
    return getPagesResult(p,paginator.num_pages,True,result=result)
def browseVersionGetCached(keyword,today,p):
    key='browseVersionResult1%s_%s_%d'%(keyword,today,p)
    return cache.get(key,None)
    #return  None
def browseVersionSetCached(keyword,today,p,result,page_count):
    key='browseVersionResult1%s_%s_%d'%(keyword,today,p)
    cache.set(key,[result,page_count],30)
def browseVersionForTemplates(request):
    try:
        p=int(request.REQUEST.get('p','1'))
    except ValueError:
        p=1
    if request.method=='POST' :
        keyword=request.POST.get('keyword','')
        today=(request.POST.get('today','').lower()=='true')
        request.session['keyword']=keyword
        request.session['today']=today
    else:
        keyword=request.session.get('keyword','')
        today=request.session.get('today',False)
    c=browseVersionGetCached(keyword,today,p)
    if c:
        result=c[0]
        page_count=c[1]
    else:

        start= datetime.date.today()
        if today:
                list=VBrows.objects.filter(Q(version_createTime__gt=start)&(Q(fullName__icontains=keyword)|Q(parentFullName__icontains=keyword)|Q(description__icontains=keyword)))
        else:
            list=VBrows.objects.filter(Q(fullName__icontains=keyword)|Q(parentFullName__icontains=keyword)|Q(description__icontains=keyword))
        result=[]
        paginator=Paginator(list,50)
        try:
            versions=paginator.page(p)
        except (EmptyPage, InvalidPage):
            p=paginator.num_pages
            versions=paginator.page(paginator.num_pages)
        page_count=paginator.num_pages
        lastBranch=''
        lastSubBranch=''
        for b in versions:
            branch_name=b.branch_name
            subbranch_full_name="%s-%s"%(b.branch_name,b.subbranch_name)
            if not lastBranch==branch_name:
                lastSubBranch=''
                lastBranch=branch_name
                item={
                    'type':'branch',
                    'branch_name':branch_name,
                    'branch_desc':b.subbranch_description,
                }
                result.append(item)
            if not lastSubBranch==subbranch_full_name:
                lastSubBranch=subbranch_full_name
                item={
                    'type':'subbranch',
                    'subbranch_name':subbranch_full_name,
                    'subbranch_desc':b.branch_description,
                }
                result.append(item)
            item={
                'type':'version',
                'version_fullname':b.fullName,
                'version_base':b.parentFullName,
                'version_desc':b.description,
                'time':b.version_createTime,
                'url':getDownloadUrl(b.fullName)
            }
            result.append(item)
        browseVersionSetCached(keyword,today,p,result,page_count)
    return render_to_response('browseVersionForTemplates.html',locals())

def home(request):
    return HttpResponseRedirect("/version/browseVersion.py")

def splitVersion(v):
    v=v.replace('.zip','')
    if not v.find('eng_') ==-1 :
        isEng=True
    else:
        isEng=False
    v=v.replace('user_','').replace('eng_','')
    r=re.compile(r"([^-_]+_[^-_]+_[^-_]+)-([^-_]+)_(.*)")
    m=r.match(v)
    if m :
        groups=m.groups()
        branch=groups[0]
        suBranch=groups[1]
        timestamp=groups[2]
        return isEng,branch,suBranch,timestamp
    else:
        r=re.compile(r"([^-_]+_[^-_]+_[^-_]+)_(.*)")
        m=r.match(v)
        if m :
            groups=m.groups()
            branch=groups[0]
            suBranch=''
            timestamp=groups[1]
            return isEng,branch,suBranch,timestamp

    return  None,None,None,None

def versionLog(request):
    if request.method=='POST' :
        fullname=request.POST.get('v')
        if fullname :
            fullname=fullname.replace('.zip','')
            isEng,branch,suBranch,timestamp=splitVersion(fullname)
            if branch :
                vl=VersionLog()
                vl.engVersion=isEng
                vl.branchName=branch
                vl.subBranchName=suBranch
                vl.timestamp=timestamp
                vl.versionFullName=fullname
                vl.save()
        return getResult(True)
    else:
        try:
            p=int(request.REQUEST.get('p','1'))
        except ValueError:
            p=1
        all_logs=VersionLog.objects.all().order_by('-datetime')
        paginator=Paginator(all_logs,50)
        pageCount=paginator.num_pages
        try:
            logs=paginator.page(p)
        except (EmptyPage, InvalidPage):
            p=paginator.num_pages
            logs=paginator.page(paginator.num_pages)

        return render_to_response('versionLog.html',locals())

def version_names(request):
    if request.method=='POST':
        ids=request.POST.getlist('id')
        names=[]
        for id in ids:
            try:
                log=VersionLog.objects.get(pk=id)
                names.append(log.versionFullName)
            except:
                pass
        names.sort()

    return  render_to_response('version_names.html',locals())

