from django.conf.urls import patterns, include, url
urlpatterns = patterns('main.views',
    url(r'^$', 'home'),
    url(r'^manage/$', 'admin'),
    url(r'^manage/newsite/$', 'newsite'),
    url(r'^manage/updatesite/(?P<pk>\d+)/$', 'updatesite'),
    url(r'^manage/deletesite/(?P<pk>\d+)/$', 'deletesite'),
    url(r'^manage/newaccount/$', 'newaccount'),
)
