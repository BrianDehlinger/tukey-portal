from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import api

from horizon.dashboards.nova.images_and_snapshots.views import IndexView as OldIndexView

from tukey.dashboards.nova.images_and_snapshots.images.tables import ImagesTable
from tukey.dashboards.nova.images_and_snapshots.snapshots.tables import SnapshotsTable

#from horizon.dashboards.nova.images_and_snapshots.images.tables import ImagesTable
#from horizon.dashboards.nova.images_and_snapshots.snapshots.tables import SnapshotsTable

class IndexView(OldIndexView):

    table_classes = (ImagesTable, SnapshotsTable)

    def get_images_data(self):
        marker = self.request.GET.get(ImagesTable._meta.pagination_param, None)
        try:
            # FIXME(gabriel): The paging is going to be strange here due to
            # our filtering after the fact.
            (all_images,
             self._more_images) = api.image_list_detailed(self.request,
                                                          marker=marker)

            images = [im for im in all_images
                      if im.container_format not in ['aki', 'ari'] and
                      im.properties.get("image_type", '') != "snapshot"]

            euca_ids = ('emi','eki','eri')

            if marker and marker.startswith(euca_ids):
                images = [im for im in images
                      if im.id.startswith(euca_ids)]

        except:
            images = []
            exceptions.handle(self.request, _("Unable to retrieve images."))
        return images

