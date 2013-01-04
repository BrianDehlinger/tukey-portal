from django.conf.urls import patterns, include, url

urlpatterns = patterns('tukey.keyservice.views',
    url(r'^$', 'keyservice', name='keyservice_index'),
    url(r'^add_repository/$', 'add_repository'),
    url(r'^add_key/$', 'add_key'),      
    url(r'^(?P<key>\w+:/[\w/\-]+)/$', 'keyservice_lookup'), 
    url(r'^(?P<key>.*)/$', 'keyservice_invalid'),         	    
)
