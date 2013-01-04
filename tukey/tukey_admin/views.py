# views.py

from horizon import api
from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import tables
from horizon import workflows

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _


from .models import Login, LoginShibboleth, LoginOpenid
from .tables import LoginsTable, LoginShibbolethsTable, LoginOpenidsTable
from .forms import CreateLoginShibbolethForm, CreateLoginOpenidForm, CreateLoginForm



class PaginatedView(tables.DataTableView):

    entries_per_page = 14

    def has_more_data(self, table):
        return getattr(self, "_more_%s" % table.name, False)

    def get_paginated_data(self, model):
	database = self.request.GET.get('cloud', 'openstack_login')

        marker = self.request.GET.get(self.__class__.table_class._meta.pagination_param, None)
        try:
            marker = int(marker)
        except TypeError:
            marker = 0
	except ValueError:
	    marker = 0

        entry_set = model.objects.using(database).filter(userid__gt=marker)
	table_name = self.__class__.table_class._meta.name
        setattr(self, "_more_%s" % table_name, entry_set.count() > PaginatedView.entries_per_page)
        data = [entry for entry in entry_set.all()[:PaginatedView.entries_per_page]]

        return data



class LoginView(PaginatedView):
    table_class = LoginsTable

    template_name = 'osdc/tukey_admin/login.html'

    def get_data(self):
        return self.get_paginated_data(Login)


class LoginShibbolethView(PaginatedView):
    table_class = LoginShibbolethsTable

    template_name = 'osdc/tukey_admin/login_shibboleth.html'

    def get_data(self):
        return self.get_paginated_data(LoginShibboleth)


class LoginOpenidView(PaginatedView):
    table_class = LoginOpenidsTable

    template_name = 'osdc/tukey_admin/login_openid.html'

    def get_data(self):
        return self.get_paginated_data(LoginOpenid)


class CreateLoginOpenidView(forms.ModalFormView):
    form_class = CreateLoginOpenidForm
    template_name = 'osdc/tukey_admin/create_login_openid.html'
    context_object_name = 'login_openid'
    success_url = reverse_lazy("tukey_admin:login_openid")
    
class CreateLoginView(forms.ModalFormView):
    form_class = CreateLoginForm
    template_name = 'osdc/tukey_admin/create_login.html'
    context_object_name = 'login'
    success_url = reverse_lazy("tukey_admin:login")
    
class CreateLoginShibbolethView(forms.ModalFormView):
    form_class = CreateLoginShibbolethForm
    template_name = 'osdc/tukey_admin/create_login_shibboleth.html'
    context_object_name = 'login_shibboleth'
    success_url = reverse_lazy("tukey_admin:login_shibboleth")
    
