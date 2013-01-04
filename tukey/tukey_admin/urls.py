#from django.conf.urls import patterns, include, url
#
#urlpatterns = patterns('files.views',
#    url(r'^$', 'files'),
#)
from django.conf.urls.defaults import patterns, url

from .views import LoginView, LoginShibbolethView, LoginOpenidView, CreateLoginView, CreateLoginShibbolethView, CreateLoginOpenidView


urlpatterns = patterns('files.views',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login_shibboleth/$', LoginShibbolethView.as_view(), name='login_shibboleth'),
    url(r'^login_openid/$', LoginOpenidView.as_view(), name='login_openid'),
    # creation urls
    url(r'^create_login/$', CreateLoginView.as_view(), name='create_login'),
    url(r'^create_login_shibboleth/$', CreateLoginShibbolethView.as_view(), name='create_login_shibboleth'),
    url(r'^create_login_openid/$', CreateLoginOpenidView.as_view(), name='create_login_openid'),
)


#urlpatterns = patterns('',
#    url(r'^$',
#        ListView.as_view(
#            queryset=FilesystemUser.objects.using('files').all(),
#            context_object_name='users',
#            template_name='osdc/files/files.html'),
#        name='files'),


#    url(r'^(?P<pk>\d+)/$',
#        DetailView.as_view(
#            model=Poll,
#            template_name='polls/detail.html'),
#        name='poll_detail'),
#    url(r'^(?P<pk>\d+)/results/$',
#        DetailView.as_view(
#            model=Poll,
#            template_name='polls/results.html'),
#        name='poll_results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),

#)
