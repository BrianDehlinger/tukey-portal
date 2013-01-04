from django.conf import settings

import memcache

# used for all clouds by monkey-patching the cloud datatables ojects
# found in tables.py also requires modifications to html templates

# Example:
#    from tukey.cloud_attribute import get_cloud
#    table_class.cloud = tables.Column(get_cloud, verbose_name=_("Cloud"))

#TODO: transition to a cloudname and cloud if tags
def get_cloud(cloud_object):
    if hasattr(cloud_object, 'cloud'):
        cloud = cloud_object.cloud
        return cloud

    elif hasattr(cloud_object, '_info'):
	if 'cloud' in cloud_object._info:
	    cloud = cloud_object._info['cloud']
	    return cloud

    elif hasattr(cloud_object._apiresource, 'cloud'):
        cloud = cloud_object._apiresource.cloud
        return cloud
    return 'Not available'


def get_cloud_id(cloud_object):
    if hasattr(cloud_object, 'cloud_id'):
        cloud = cloud_object.cloud
        return cloud

    elif hasattr(cloud_object, '_info'):
	if 'cloud_id' in cloud_object._info:
	    cloud = cloud_object._info['cloud_id']
	    return cloud

    elif hasattr(cloud_object._apiresource, 'cloud_id'):
        cloud = cloud_object._apiresource.cloud_id
        return cloud
    return 'Not available'



# will require some sort of context for querying an api or reading
# a config file to see what the names are of the clouds
# For now it is a stub 
def cloud_details(user):

    active = active_clouds(user)

    return {key: value for key, value in settings.CLOUD_DETAILS.items()
	    if key in active or key.startswith('login') 
        and key[5:] in active or key == 'all'}

def has_function(function, cloud):
    return cloud in settings.CLOUD_FUNCTIONS[function]

def active_clouds(user):

    others = ['openstack', 'fake_tenant', 'fake_endpoint']

    mc = memcache.Client([settings.AUTH_MEMCACHED], debug=0)
    creds = mc.get(str(user.token.token['id']))

    return [key for key in creds.keys() if key not in others]
