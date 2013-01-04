import logging

from django.conf import settings
from openid.consumer.consumer import SUCCESS
from openid.extensions import pape

from django_openid_auth import teams
from django_openid_auth.models import UserOpenID
from django_openid_auth.exceptions import (
    MissingPhysicalMultiFactor,
    RequiredAttributeNotReturned,
)

from django_openid_auth.forms import OpenIDLoginForm

from openstack_auth.backend import KeystoneBackend

from django_openid_auth.views import (
    login_begin as old_login_begin,
    default_render_failure,
    REDIRECT_FIELD_NAME
)

from django.contrib.auth.models import AnonymousUser
from openstack_auth.exceptions import KeystoneAuthException

from .models import UnregisteredUser

from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django_openid_auth.auth import OpenIDBackend

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, authenticate, login as auth_login)
from django_openid_auth.signals import openid_login_complete
from django_openid_auth.exceptions import (
    DjangoOpenIDException,
)

from django_openid_auth.views import (
    parse_openid_response,
    sanitise_redirect_url,
)

LOG = logging.getLogger(__name__)


class OpenIDKeystoneBackend(KeystoneBackend):

    def __init__(self):
        self.openid_backend = OpenIDBackend()

    def authenticate(self, **kwargs):
        """Authenticate the user based on an OpenID response."""
        # Require that the OpenID response be passed in as a keyword
        # argument, to make sure we don't match the username/password
        # calling conventions of authenticate.

        openid_response = kwargs.get('openid_response')
        if openid_response is None:
            return None

        if openid_response.status != SUCCESS:
            return None

        user = None
        try:
            user_openid = UserOpenID.objects.get(
                claimed_id__exact=openid_response.identity_url)
        except UserOpenID.DoesNotExist:
            if getattr(settings, 'OPENID_CREATE_USERS', False):
                user = self.create_user_from_openid(openid_response)
        else:
            user = user_openid.user

        if user is None:
            return None

        #if getattr(settings, 'OPENID_UPDATE_DETAILS_FROM_SREG', False):
        details = self._extract_user_details(openid_response)
        self.update_user_details(user, details, openid_response)

        if getattr(settings, 'OPENID_PHYSICAL_MULTIFACTOR_REQUIRED', False):
            pape_response = pape.Response.fromSuccessResponse(openid_response)
            if pape_response is None or \
               pape.AUTH_MULTI_FACTOR_PHYSICAL not in pape_response.auth_policies:
                raise MissingPhysicalMultiFactor()

        teams_response = teams.TeamsResponse.fromSuccessResponse(
            openid_response)
        if teams_response:
            self.update_groups_from_teams(user, teams_response)
            self.update_staff_status_from_teams(user, teams_response)

	LOG.debug("email %s:", details['email'])


	try:
		user = super(OpenIDKeystoneBackend, self).authenticate(password='openid', 
		    username=details['email'], auth_url=settings.OPENSTACK_KEYSTONE_URL,
		    request=kwargs.get('request'))

	except KeystoneAuthException:
	    LOG.debug("KeystoneAuth exception returning UnregisteredUser")
	    return UnregisteredUser('OpenID', details['email'])

	LOG.debug("USER: %s", user)
	LOG.debug("user.id: %s", user.id)
	LOG.debug("user token: %s", user.token)
	LOG.debug("endpoint %s", user.endpoint)
	LOG.debug(" %s", dir(self))
	
        return user


    def _extract_user_details(self, openid_response):
	return self.openid_backend._extract_user_details(openid_response)
 

    def _get_available_username(self, nickname, identity_url):
	return self.openid_backend._get_available_username(nickname, identity_url)


    def create_user_from_openid(self, openid_response):
	return self.openid_backend.create_user_from_openid(openid_response)


    def associate_openid(self, user, openid_response):
	return self.openid_backedn.associate_openid(user, openid_response)


    def update_user_details(self, user, details, openid_response):
	return self.openid_backend.update_user_details(user, details,
	    openid_response)


    def update_groups_from_teams(self, user, teams_response):
	return self.openid_backend.update_groups_from_teams(user, teams_response)


    def update_staff_status_from_teams(self, user, teams_response):
	return self.openid_backend.update_staff_status_from_teams(user,
	    teams_response)


def login_begin(request, template_name='openid/login.html',
                login_complete_view='openid:openid-complete',
                form_class=OpenIDLoginForm,
                render_failure=default_render_failure,
                redirect_field_name=REDIRECT_FIELD_NAME):

    LOG.debug('new login begin')
    return old_login_begin(request, 
	settings.ROOT_PATH + '/../tukey/templates/osdc/openid_login.html', login_complete_view,
	form_class, render_failure, redirect_field_name)



# replace login complete so that if the user is not
# authenticated this will send them to the page 
# where they can register

def login_complete(request, redirect_field_name=REDIRECT_FIELD_NAME,
                   render_failure=None):
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    render_failure = render_failure or \
                     getattr(settings, 'OPENID_RENDER_FAILURE', None) or \
                     default_render_failure

    openid_response = parse_openid_response(request)
    if not openid_response:
        return HttpResponseRedirect(sanitise_redirect_url(redirect_to))
#        return render_failure(
#            request, 'This is an OpenID relying party endpoint.')

    if openid_response.status == SUCCESS:
        try:
            user = authenticate(openid_response=openid_response)
        except DjangoOpenIDException, e:
	    return HttpResponseRedirect(sanitise_redirect_url(redirect_to))
#            return render_failure(request, e.message, exception=e)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                response = HttpResponseRedirect(sanitise_redirect_url(redirect_to))

                # Notify any listeners that we successfully logged in.
                openid_login_complete.send(sender=UserOpenID, request=request,
		    user=user,
                    openid_response=openid_response)

                return response
            else:
		from tukey.views import register_user
	    	return register_user(request, user)

    return HttpResponseRedirect(sanitise_redirect_url(redirect_to))
#
#                #return render_failure(request, 'Disabled account')
#        else:
#            return render_failure(request, 'Unknown user')
#    elif openid_response.status == FAILURE:
#        return render_failure(
#            request, 'OpenID authentication failed: %s' %
#            openid_response.message)
#    elif openid_response.status == CANCEL:
#        return render_failure(request, 'Authentication cancelled')
#    else:
#        assert False, (
#            "Unknown OpenID response type: %r" % openid_response.status)
#
