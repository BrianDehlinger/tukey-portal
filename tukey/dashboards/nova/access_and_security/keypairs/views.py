import logging

from django import http
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.views.generic import View, TemplateView
from django.utils.translation import ugettext_lazy as _

from horizon.dashboards.nova.access_and_security.keypairs.views import (
    CreateView as OldCreateView,
    ImportView as OldImportView,
    DownloadView as OldDownloadView)

LOG = logging.getLogger(__name__)


class CreateView(OldCreateView):

    def get_success_url(self):
        #append on the cloud name to to go through the nova api 
        #and be switched by the middlewarea
        print "THIS ONE WAS CALLED"
        cloud_and_name = self.request.POST['cloud'] + '-' + self.request.POST['name']
        return reverse(self.success_url,
                       kwargs={"keypair_name": cloud_and_name})


class ImportView(OldImportView):

    def get_object_id(self, keypair):
        #append on the cloud name to to go through the nova api
        #and be switched by the middleware
        return self.request.POST['cloud'] + '-' + keypair.name


class DownloadView(OldDownloadView):
    def get_context_data(self, keypair_name=None):
        return {'keypair_name': keypair_name,
        'display_name': '-'.join(keypair_name.split('-')[1:]) }
