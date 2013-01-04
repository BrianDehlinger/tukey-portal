from horizon.dashboards.nova.access_and_security.views import IndexView as OldIndexView

from tukey.dashboards.nova.access_and_security.keypairs.tables import KeypairsTable

class IndexView(OldIndexView):
    table_classes = (KeypairsTable,)
