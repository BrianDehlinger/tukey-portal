from horizon import api
from horizon import exceptions

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _


from horizon.dashboards.nova.instances.views import DetailView as OldDetailView
from horizon.dashboards.nova.instances.views import IndexView as OldIndexView

from .tables import InstancesTable

class IndexView(OldIndexView):
    table_class = InstancesTable
    template_name = 'nova/instances/index.html'


class DetailView(OldDetailView):

    def get_context_data(self, **kwargs):
        context = super(OldDetailView, self).get_context_data(**kwargs)
        context["instance"] = self.get_data()
        return context

    def get_data(self):
        if not hasattr(self, "_instance"):
            try:
                instance_id = self.kwargs['instance_id']
                instance = api.server_get(self.request, instance_id)
                #instance.volumes = api.volume_instance_list(self.request,
                #                                            instance_id)
                # Sort by device name
                #instance.volumes.sort(key=lambda vol: vol.device)
                instance.full_flavor = api.flavor_get(self.request,
                                                      instance.flavor["id"])
                instance.security_groups = api.server_security_groups(
                                           self.request, instance_id)
            except:
                redirect = reverse('horizon:nova:instances:index')
                exceptions.handle(self.request,
                                  _('Unable to retrieve details for '
                                    'instance "%s".') % instance_id,
                                    redirect=redirect)
            self._instance = instance
        return self._instance
