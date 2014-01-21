from version.views import *

__author__ = 'fanjunwei003'
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('version/',
                       url(r'^login.py$', login),
                       url(r'^main.py$', main),
                       url(r'^manageBranch.py$', manageBranch),
                       url(r'^saveBranch.py$', saveBranch),
                       url(r'^getBranches.py$', getBranches),
                       url(r'^delBranches.py$', delBranches),

                       url(r'^manageSubBranch.py$', manageSubBranch),
                       url(r'^searchBranchesName.py$', searchBranchesName),
                       url(r'^getSubBranches.py$', getSubBranches),
                       url(r'^saveSubBranch.py$', saveSubBranch),
                       url(r'^delSubBranches.py$', delSubBranches),

                       url(r'^manageVersion.py$', manageVersion),
                       url(r'^getVersions.py$', getVersions),
 )
