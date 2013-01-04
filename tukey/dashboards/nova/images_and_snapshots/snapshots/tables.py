from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.core.urlresolvers import reverse


from horizon import tables

from horizon.dashboards.nova.images_and_snapshots.snapshots.tables import (
    SnapshotsTable as OldSnapshotsTable,
    LaunchSnapshot as OldLaunchSnapshot,
    DeleteSnapshot)

from horizon.dashboards.nova.images_and_snapshots.snapshots.tables import EditImage, UpdateRow

from tukey.cloud_attribute import get_cloud


class LaunchSnapshot(OldLaunchSnapshot):

    def get_link_url(self, datum):
        base_url = reverse(self.url)
        params = urlencode({"source_type": "instance_snapshot_id",
                "cloud": get_cloud(datum),
                            "source_id": self.table.get_object_id(datum)})
        return "?".join([base_url, params])



class SnapshotsTable(OldSnapshotsTable):
    cloud = tables.Column(get_cloud, verbose_name=_("Cloud"))

    class Meta:
        name = "snapshots"
        verbose_name = _("Instance Snapshots")
        table_actions = (DeleteSnapshot,)
        row_actions = (LaunchSnapshot, EditImage, DeleteSnapshot)
        pagination_param = "snapshot_marker"
        row_class = UpdateRow
        status_columns = ["status"]
