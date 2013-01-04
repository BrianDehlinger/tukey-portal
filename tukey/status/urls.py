from django.conf.urls import patterns, include, url

urlpatterns = patterns('tukey.status.views',
    url(r'^$', 'status_public'),
)

