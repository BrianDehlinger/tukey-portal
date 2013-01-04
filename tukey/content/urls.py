from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
#    url(r'^$', 'tukey.content.views.index'),
    url(r'^(?P<slug>[-\w]*)/$', 'tukey.content.views.page'),
    #url(r'^(?P<slug>[-\w]*)$', 'tukey.content.views.page'),
)
