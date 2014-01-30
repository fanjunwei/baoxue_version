import cookielib
import urllib2
import urllib

__author__ = 'fanjunwei003'
UserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'
branches="""F10_BXT_51
F10_BXT_53
F10_HWD_03
F10_HWD_51
F10_HWD_52
F10_HWD_53
F10_TJTC_01
F18_BXT_01
F18_BXT_51
F22_BXT_51
F22_BXT_52
F22_BXT_53
F22_BXT_54
F22_ZTC_51
F35_BXT_51
F35_CDL_51
F35_DSK_51
F35_DSK_53
F35_HNS_51
F35_KCD_51
F35_YL_51
F35_YL_52
F35_YL_53
F35_YX_51
F35_YX_52
F35_YX_53
F35_ZXS_51
F6_BXT_01
F6_BXT_03
F6_JHL_01
F6_LQD_51
F6_SJT_01
F6_YX_51
F6_YX_52
F6_ZTC_51
F6_ZTC_52
F7_BXT_01
F7_BXT_02
F7_BXT_03
F7_XLH_01
F8_BXT_03
F8_BXT_51
F9_BXT_01
F9_BXT_03
A222_BXT_01
A22_BXT_01
A22_BXT_01V3
A22_BXT_11
A22_BXT_12
A22_BXT_12V3
A22_BXT_13
A22_BXT_13V3
A22_BXT_14
A22_SK_12V3
A35_BXT_11
A35_BXT_11V2
A35_HNS_11
A35_HNS_11V2
A35_HNS_13V2
A35_YL_11
A35_ZXS_11V2
A6_BXT_11
"""

def post(url,parms):
    data = urllib.urlencode(parms)
    headers={
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': UserAgent
    }
    req=urllib2.Request(url,data,headers)
    response=urllib2.urlopen(req)
    return response.read()

def get(url):
    headers={
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': UserAgent
    }
    req=urllib2.Request(url,None,headers)
    response=urllib2.urlopen(req)
    return response.read()

for b in  branches.split('\n'):
    #http://192.168.1.2:8000/version/saveBranch.py
    #id,name,description
    print post('http://192.168.1.2:8000/version/saveBranch.py',{'id':'','name':b,'description':''})