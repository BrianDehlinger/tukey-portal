# tables.py
import logging

from django import template
from django.core import urlresolvers
from django.template.defaultfilters import title
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.templatetags import sizeformat
from horizon.utils.filters import replace_underscores

from .models import Login, LoginShibboleth, LoginOpenid



LOG = logging.getLogger(__name__)


class DestroyAction(tables.DeleteAction):
    classes = ('btn-danger', 'btn-delete')

    def delete_model(self, user, ids, model):
        f_user = FilesystemUser.objects.using('files').filter(f_name=user)[0]
        for id in ids:
            g = model(id=id, owner=f_user)
            g.delete()


class DeleteAction(DestroyAction):
    name = "delete"
    action_present = _("Delete")
    action_past = _("Deleted")


class RemoveAction(DestroyAction):
    name = "remove"
    action_present = _("Remove")
    action_past = _("Removed")


class EditAction(tables.LinkAction):
    name = "edit"
    action_present = _("Edit")
    action_past = _("Edited")
    classes = ('btn')


class NewLink(tables.LinkAction):
    name = "new"
    classes = ("ajax-modal", "btn-create")

class NewLogin(NewLink):
    verbose_name = _("New Login")
    url = "tukey_admin:create_login"


class NewLoginShibboleth(NewLink):
    verbose_name = _("Add Shibboleth Info to Login")
    url = "tukey_admin:create_login_shibboleth"

class NewLoginOpenid(NewLink):
    verbose_name = _("Add Openid Info to Login")
    url = "tukey_admin:create_login_openid"

class DeleteLogin(DeleteAction):
    data_type_singular = _("Login")
    data_type_plural = _("Logins")

    def handle(self, table, request, obj_ids):
        self.delete_model(request.user, obj_ids, Login)


class RemoveLoginShibboleth(RemoveAction):
    data_type_singular = _("Shibboleth Info from Login")
    data_type_plural = _("Shibboleth Info from Logins")

    def handle(self, table, request, obj_ids):
        self.delete_model(request.user, obj_ids, LoginShibboleth)


class RemoveLoginOpenid(RemoveAction):
    data_type_singular = _("Openid Info from Login")
    data_type_plural = _("Openid Info from Logins")

    def handle(self, table, request, obj_ids):
        self.delete_model(request.user, obj_ids, LoginOpenid)


def get_login(item):
    return item.username

def get_username(item):
    return item.userid.username

def get_password(item):
    return item.password

def get_shibboleth(item):
    return item.eppn

def get_openid(item):
    return item.openid


class LoginsTable(tables.DataTable):

    name = tables.Column(get_login,
        verbose_name = _("Username"))

    password = tables.Column(get_password,
        verbose_name = _("Password"))

    class Meta:
        name = "logins"
        verbose_name = _("Logins")
        row_actions = (DeleteLogin,)
	table_actions = (NewLogin, DeleteLogin)
	pagination_param = 'login_marker'


class LoginShibbolethsTable(tables.DataTable):

    login = tables.Column(get_username,
        verbose_name = _("Login"))
        
    shibboleth = tables.Column(get_shibboleth,
        verbose_name = _("Shibboleth Info"))

    class Meta:
        name = "login_shibboleths"
        verbose_name = _("Shibboleth Info for Logins")
        row_actions = (RemoveLoginShibboleth,)
	table_actions = (NewLoginShibboleth, RemoveLoginShibboleth)
	pagination_param = 'login_shibboleth_marker'

        
class LoginOpenidsTable(tables.DataTable):

    login = tables.Column(get_username,
        verbose_name = _("Login"))
        
    openid = tables.Column(get_openid,
        verbose_name = _("Openid Info"))

    class Meta:
        name = "login_openids"
        verbose_name = _("Openid Info for Logins")
        row_actions = (RemoveLoginOpenid,)
	table_actions = (NewLoginOpenid, RemoveLoginOpenid)
	pagination_param = 'login_openid_marker'

