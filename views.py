import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from geonode import settings


class OAuthToolkitAdapter(OAuth2Adapter):
    provider_id = "oauthtoolkitprovider"

    # Fetched programmatically, must be reachable from container
    access_token_url = '{}/api/o/token/'.format(settings.OAUTH_SERVER_BASEURL_INTERNAL)
    profile_url = '{}/api/auth/userdetails/'.format(settings.OAUTH_SERVER_BASEURL_INTERNAL)
    authorize_url = '{}/api/o/authorize/'.format(settings.OAUTH_SERVER_BASEURL_PUBLIC)

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': f'Bearer {token.token}', 'Accept':'application/json'}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(OAuthToolkitAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(OAuthToolkitAdapter)