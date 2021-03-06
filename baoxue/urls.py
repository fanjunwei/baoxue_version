from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from baoxue import settings
from version.views import home

admin.autodiscover()
urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', home),
                       # url(r'^baoxue/', include('baoxue.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^version/', include('version.urls')),
                       url(r'^downloadUrl/(?P<fullName>.*?)$', 'version.views.downloadUrl', name='downloadUrl'),
                       url(r"^check_web_access/(?P<version>.*?)$", 'version.views.check_web_access'),
                       # url(r'^static/(?P<path>.*)$','django.views.static.serve',{settings.STATIC_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()
