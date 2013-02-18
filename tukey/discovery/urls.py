from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^disco.json$', views.discoFeed, name='disco.json'),
    url(r'^idpselect_config.js$', views.config, name='config'),
    url(r'^idpselect.js$', views.idpselect, name='idpselect'),
#    url(r'^query/$', views.query, name='query'),
)

