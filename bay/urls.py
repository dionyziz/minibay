from django.conf.urls import patterns, url

from bay import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/(?P<text>.*)$', views.search, name='search'),
    url(r'^download/(?P<id>\d+)$', views.download, name='download'),
    url(r'^listen/(?P<file_id>\d+)$', views.listen, name='listen'),
)
