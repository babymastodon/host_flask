from django.conf.urls import patterns, include, url
urlpatterns = patterns('main.views',
    url(r'^$', 'home'),
    url(r'^admin/$', 'admin'),
    url(r'^newsite/$', 'newsite'),
    url(r'^updatesite/(?P<pk>\d+)/$', 'updatesite'),
    url(r'^deletesite/(?P<pk>\d+)/$', 'deletesite'),
    url(r'^newaccount/$', 'login_page'),
)
