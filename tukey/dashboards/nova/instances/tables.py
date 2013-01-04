from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from tukey.cloud_attribute import get_cloud

from horizon import tables

from horizon.dashboards.nova.instances.tables import (
    InstancesTable as OldInstancesTable,
    AssociateIP, EditInstance, TerminateInstance)


class LaunchLink(tables.LinkAction):
    name = "launch"
    verbose_name = _("Launch Instance")
    url = "horizon:nova:images_and_snapshots:index"

class InstancesTable(OldInstancesTable):

    cloud = tables.Column(get_cloud, verbose_name=_("Cloud"))

    Meta = OldInstancesTable.Meta
    Meta.table_actions = (LaunchLink, TerminateInstance)


def edit_instance_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['edit_instance']

EditInstance.allowed = edit_instance_allowed

def associate_ip_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['associate_ip']

AssociateIP.allowed = associate_ip_allowed
