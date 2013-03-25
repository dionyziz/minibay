from django.conf.urls import patterns, url

from bay import views

urlpatterns = patterns('',
    url(r'^$', views.homepage, name='homepage'),
    url(r'^search/(?P<q>.*)$', views.search, name='search'),
    url(r'^download/(?P<id>\d+)$', views.song_download, name='song_download'),
    url(r'^listen/(?P<file_id>\d+)(/(?P<q>.*))?$', views.player, name='player'),
)
