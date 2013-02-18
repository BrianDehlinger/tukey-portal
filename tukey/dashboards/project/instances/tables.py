from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from tukey.cloud_attribute import get_cloud

from openstack_dashboard.dashboards.project.instances.tables import (
    InstancesTable as OldInstancesTable,
    AssociateIP, SimpleAssociateIP, SimpleDisassociateIP, EditInstance, TerminateInstance)


class LaunchLink(tables.LinkAction):
    name = "launch"
    verbose_name = _("Launch Instance")
    url = "horizon:project:images_and_snapshots:index"

class InstancesTable(OldInstancesTable):

    cloud = tables.Column(get_cloud, verbose_name=_("Cloud"))

    Meta = OldInstancesTable.Meta
    Meta.table_actions = (LaunchLink, TerminateInstance)


old_edit_instance_allowed = EditInstance.allowed

def edit_instance_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['edit_instance'] \
        and old_edit_instance_allowed(self, request, instance)

EditInstance.allowed = edit_instance_allowed


old_associate_ip_allowed = AssociateIP.allowed

def associate_ip_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['associate_ip'] \
        and old_associate_ip_allowed(self, request, instance)

AssociateIP.allowed = associate_ip_allowed


old_simple_associate_ip_allowed = SimpleAssociateIP.allowed

def simple_associate_ip_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['associate_ip'] \
        and old_simple_associate_ip_allowed(self, request, instance)

SimpleAssociateIP.allowed = simple_associate_ip_allowed


old_simple_disassociate_ip_allowed = SimpleDisassociateIP.allowed

def simple_disassociate_ip_allowed(self, request, instance=None):

    return get_cloud(instance).lower() in settings.CLOUD_FUNCTIONS['associate_ip'] \
        and old_simple_disassociate_ip_allowed(self, request, instance)

SimpleDisassociateIP.allowed = simple_disassociate_ip_allowed

