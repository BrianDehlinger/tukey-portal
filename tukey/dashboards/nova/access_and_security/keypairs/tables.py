from horizon import tables

from django.utils.translation import ugettext_lazy as _

from tukey.cloud_attribute import get_cloud, get_cloud_id

from horizon.dashboards.nova.access_and_security.keypairs.tables import KeypairsTable as OldKeypairsTable

class KeypairsTable(OldKeypairsTable):

    # Thie should be somewhere else but I just don't know where
    # mgreenway
    cloud = tables.Column(get_cloud, verbose_name=_("Resource"))
    #end modified section mgreenway

    def get_object_id(self, keypair):
        #return get_cloud(keypair).lower() + '-' + keypair.name
        return get_cloud_id(keypair) + '-' + keypair.name

    Meta = OldKeypairsTable.Meta
