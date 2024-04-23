# ---------------------------------------------------------------------------- #
#                                 DJANGO VIEWS                                 #
# ---------------------------------------------------------------------------- #


# Dependencies import
import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import CustomProvider
from geonode import settings

# Logging
import logging
logger = logging.getLogger('ohworker_auth')

# ---------------------------------------------------------------------------- #
#                         OAUTH2 GEONODE AUTHENTICATION                        #
# ---------------------------------------------------------------------------- #

class CustomAdapter(OAuth2Adapter):
    """This class is useful to enable OAUTH2 authentication against Geonode provider.
    Refer to documentation [HERE](https://petersimpson.dev/blog/django-allauth-custom-provider/)
    """
    provider_id = CustomProvider.id
    
    # Fetched programmatically, must be reachable from container
    access_token_url = '{}/o/token/'.format(settings.OAUTH_SERVER_BASEURL)
    profile_url = '{}/userdetails/'.format(settings.OAUTH_SERVER_BASEURL)
    
    # Accessed by the user browser, must be reachable by the host
    authorize_url = '{}/o/authorize/'.format(settings.OAUTH_SERVER_BASEURL)

    # NOTE: trailing slashes in URLs are important, don't miss it
    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        logger.debug('{data}'.format(data=str(headers)))
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)