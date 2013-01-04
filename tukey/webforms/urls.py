from django.conf.urls import patterns, include, url

urlpatterns = patterns('tukey.webforms.views',
    url(r'^apply/$', 'osdc_apply'),
    url(r'^apply/thanks/', 'osdc_apply_thanks'),                   
    url(r'^apply/invited/thanks/', 'osdc_apply_invite_thanks'),
    url(r'^apply/invited/', 'osdc_apply_invite'),                   
    url(r'^support/$', 'support'),
    url(r'^support/thanks/', 'support_thanks'),
)
