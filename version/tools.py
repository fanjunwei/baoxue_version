#coding=utf-8
import json
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
import math
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#from Sell3_server.settings import DEVICEID
import thread


def permission_required(func=None):
    def test(request, *args, **kwargs):
        if  request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return getResult(False,u'需要管理员权限')
    return test


def client_login_required(func=None):
    def test(request, *args, **kwargs):
        if not isinstance(request.user,AnonymousUser):
            if  request.user.is_active:
                # if DEVICEID:
                #     deviceid=request.REQUEST.get('deviceid',None)
                #     serverdeviceid=request.user.person.deviceid
                #     if not serverdeviceid and deviceid:
                #         from sell3.models import Person
                #         if 0==Person.objects.filter(deviceid=deviceid).count():
                #             request.user.person.deviceid=deviceid
                #             request.user.person.save()
                #         else:
                #             return getResult(False,u'设备已经使用过了，请联系管理员消除设备指纹，或使用原来的账号登录。%s_%s'%(deviceid,serverdeviceid), None,404)
                #     elif serverdeviceid and deviceid and deviceid!=serverdeviceid:
                #         return getResult(False,u'用户使用的设备与注册设备不一致，请使用注册的设备。%s_%s'%(deviceid,serverdeviceid), None,404)

                return func(request, *args, **kwargs)
            else:
                return getResult(False,u'用户已被禁用，需要重新登录。', None,404)
        else:
            return getResult(False,u'登录过期，需要重新登录。', None,404)
    return test

def getResult(success,message=None,result=None,status_code=200):
    '''
    200 正常返回 code
    404 登录过期，需要重新登录
    '''
    map={'success':success,'message':message, 'status_code':status_code}
    if result:
        map['result']=result
    return HttpResponse(json.dumps(map),'application/json')


def getPagesResult(pageIndex,pageCount,success,message=None,result=None,status_code=200):
    '''
    200 正常返回 code
    404 登录过期，需要重新登录
    '''
    map={'success':success,'message':message, 'status_code':status_code,'pageIndex':pageIndex,'pageCount':pageCount}
    if result:
        map['result']=result
    return HttpResponse(json.dumps(map),'application/json')

def rad(d):
    d=float(d)
    return d*math.pi/180.0

def distance(gps1,gps2):
    if not gps1 or not gps2:
        return 0
    gps1=gps1.split(',')
    lat1=gps1[0]
    lng1=gps1[1]
    gps2=gps2.split(',')
    lat2=gps2[0]
    lng2=gps2[1]
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s


def send_mail_thread(to_list,sub,content):
    mail_host="smtp.exmail.qq.com"
    mail_user="mantis@baoxuetech.com"
    mail_pass="baoxue1"
    mail_postfix="qq.com"
    me=mail_user
    msg = MIMEText (content,_charset='utf-8')
    msg['Subject'] = Header(sub,'utf-8')
    msg['From'] = me
    msg['To'] = ','.join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def send_mail(to_list,sub,content):
    thread.start_new_thread(send_mail_thread, (to_list,sub,content))