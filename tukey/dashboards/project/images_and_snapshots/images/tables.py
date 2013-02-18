from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard.dashboards.project.images_and_snapshots.images.tables import (
    ImagesTable as OldImagesTable,
    LaunchImage as OldLaunchImage)

from openstack_dashboard.dashboards.project.images_and_snapshots.images.tables import EditImage, UpdateRow, CreateImage, DeleteImage

from tukey.cloud_attribute import get_cloud


class LaunchImage(OldLaunchImage):

    def get_link_url(self, datum):
        base_url = reverse(self.url)
        params = urlencode({"source_type": "image_id",
                "cloud": get_cloud(datum),
                            "source_id": self.table.get_object_id(datum)})
        return "?".join([base_url, params])



class ImagesTable(OldImagesTable):
    cloud = tables.Column(get_cloud, verbose_name=_("Cloud"))

    class Meta:
        name = "images"
        row_class = UpdateRow
        status_columns = ["status"]
        verbose_name = _("Images")
        table_actions = (CreateImage, DeleteImage,)
        row_actions = (LaunchImage, EditImage, DeleteImage,)
        pagination_param = "image_marker"
