from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
import logging
logger = logging.getLogger("django")

class OAuthToolkitAccount(ProviderAccount):
    pass

class OAuthToolkitProvider(OAuth2Provider):

    id = 'oauthtoolkitprovider'
    name = 'oauthtoolkitprovider'
    account_class = OAuthToolkitAccount
    pkce_enabled_default = True

    def extract_uid(self, data):
        print('data')
        print(data)
        logger.error(data)
        return str(data['id'])

    def extract_common_fields(self, data):
        print(data)
        return dict(
            email=data['email'],
            first_name=data['username'],
        )

    def get_default_scope(self):
        scope = ['read']
        return scope

providers.registry.register(OAuthToolkitProvider)