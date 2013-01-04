from django.conf import settings
from django.utils.text import normalize_newlines
from django.utils.translation import ugettext as _

from horizon import forms

from horizon import exceptions

from horizon import api

from tukey.cloud_attribute import get_cloud

from horizon import workflows


from horizon.dashboards.nova.instances.workflows import(
    LaunchInstance as OldLaunchInstance,
    SetAccessControls,
    SetInstanceDetails,
    SetInstanceDetailsAction,
    SetAccessControlsAction,
    SelectProjectUser,
    SetInstanceDetails,
    SetAccessControls,
    #VolumeOptions,
    PostCreationStep)



class LaunchInstance(OldLaunchInstance):

    default_steps = (SelectProjectUser,
                     SetInstanceDetails,
                     SetAccessControls,
                     #VolumeOptions,
                     PostCreationStep)


    def handle(self, request, context):
        custom_script = context.get('customization_script', '')

        # Determine volume mapping options
        if context.get('volume_type', None):
            if(context['delete_on_terminate']):
                del_on_terminate = 1
            else:
                del_on_terminate = 0
            mapping_opts = ("%s::%s"
                            % (context['volume_id'], del_on_terminate))
            dev_mapping = {context['device_name']: mapping_opts}
        else:
            dev_mapping = None

        try:
            api.nova.server_create(request,
                                   context['cloud'].lower() + '-' + context['name'],
                                   context['source_id'],
                                   context['flavor'],
                                   context['keypair_id'],
                                   normalize_newlines(custom_script),
                                   context['security_group_ids'],
                                   dev_mapping,
                                   instance_count=int(context['count']))
            return True
        except:
            exceptions.handle(request)
            return False



SetInstanceDetails.contributes = ("source_type", "source_id", "name", 
    "count", "flavor", "cloud")



def populate_image_id_choices(self, request, context):

    images = self._get_available_images(request, context)


    if 'cloud' in request.GET:
        cloud = request.GET['cloud']


        if cloud.lower() not in settings.CLOUD_FUNCTIONS['launch_multiple']:
            self.fields['count'].widget.attrs['readonly'] = True

        
        if cloud.lower() not in settings.CLOUD_FUNCTIONS['namable_servers']:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['value'] = 'Feature not supported.'

        choices = [(image.id, image.name) for image in images
            if image.properties.get("image_type", '') != "snapshot"
            and (get_cloud(image) == cloud)]
    else:
        choices = [(image.id, image.name) for image in images
            if image.properties.get("image_type", '') != "snapshot"]
    if choices:
        choices.insert(0, ("", _("Select Image")))
    else:
        choices.insert(0, ("", _("No images available.")))
    return choices


def populate_flavor_choices(self, request, context):
    try:
        flavors = api.nova.flavor_list(request)

        if 'cloud' in request.GET:
            cloud = request.GET['cloud']
            flavor_list = [(flavor.id, "%s" % flavor.name)
                       for flavor in flavors
           if get_cloud(flavor) == cloud]
        else:
            flavor_list = [(flavor.id, "%s" % flavor.name)
                       for flavor in flavors]
    except:
        flavor_list = []
        exceptions.handle(request,
                          _('Unable to retrieve instance flavors.'))
    return sorted(flavor_list)


SetInstanceDetails.action_class.populate_image_id_choices = populate_image_id_choices
SetInstanceDetails.action_class.populate_flavor_choices = populate_flavor_choices


SetAccessControls.depends_on = ("project_id", "user_id", "cloud")


def populate_keypair_choices(self, request, context):
    try:
        keypairs = api.nova.keypair_list(request)
        if 'cloud' in request.GET:
            context['cloud'] = request.GET['cloud']
        if 'cloud' in context:
            cloud = context['cloud']
            keypair_list = [(kp.name, kp.name) for kp in keypairs
            if get_cloud(kp) == cloud]
        else:
            keypair_list = [(kp.name, kp.name) for kp in keypairs]
    except:
        keypair_list = []
        exceptions.handle(request,
                          _('Unable to retrieve keypairs.'))
    if keypair_list:
        keypair_list.insert(0, ("", _("Select a keypair")))
    else:
        keypair_list = (("", _("No keypairs available.")),)
    return keypair_list
    
SetAccessControlsAction.populate_keypair_choices = populate_keypair_choices
