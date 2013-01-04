# forms.py

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from .models import Login, LoginOpenid, LoginShibboleth

LOG = logging.getLogger(__name__)


class MultiDBForm(forms.SelfHandlingForm):
    database = 'openstack_login'

class CreateLoginForm(MultiDBForm):
    name = forms.CharField(max_length="255", label=_("Name"), required=True)
    password = forms.CharField(max_length="255", label=_("Password"), required=False)

    def handle(self, request, data):
        try:
	    login = Login(username=data['name'], password=data['password'])
	    login.save()
            messages.success(request,
                _('Your login %s has been created.' %
                    data['name']))
            return login
        except:
            exceptions.handle(request, _('Unable to create new login.'))


class CreateLoginShibbolethForm(MultiDBForm):

    user_name = forms.ChoiceField(label=_('User'), required=True)

    shibboleth = forms.CharField(max_length="255", label=_("Shibboleth EPPN"), required=False)

    def __init__(self, request, *args, **kwargs):
        self.base_fields['user_name'].choices = [
            (u.userid, u.username) for u in  Login.objects.using(self.database).all()]
        super(CreateLoginShibbolethForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
	    login_id = Login.objects.using(self.database).filter(username=data['user_name'])[0]
            login_shibboleth = LoginShibboleth(userid=login_id, eppn=data['shibboleth'])
            login_shibboleth.save()
            messages.success(request,
                _('Shibboleth info %s has been added to user %s.' %
                    (data['shibboleth'], data['user_name'])))
            return login_shibboleth
        except:
            exceptions.handle(request, _('Unable to add user to shibboleth.'))


class CreateLoginOpenidForm(MultiDBForm):

    user_name = forms.ChoiceField(label=_('User'), required=True)

    openid = forms.CharField(max_length="255", label=_("Openid email"), required=False)

    def __init__(self, request, *args, **kwargs):
        self.base_fields['user_name'].choices = [
            (u.userid, u.username) for u in  Login.objects.using(self.database).all()]
        super(CreateLoginOpenidForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        try:
	    login_id = Login.objects.using(self.database).filter(username=data['user_name'])[0]
            login_openid = LoginOpenid(userid=login_id, eppn=data['openid'])
            login_openid.save()
            messages.success(request,
                _('Openid info %s has been added to user %s.' %
                    (data['openid'], data['user_name'])))
            return login_openid
        except:
            exceptions.handle(request, _('Unable to add user to openid.'))


