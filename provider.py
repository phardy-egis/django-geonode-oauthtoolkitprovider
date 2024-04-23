from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

# Logging
import logging
logger = logging.getLogger(__name__)

# Custom Geonode provider
class CustomAccount(ProviderAccount):
    """
    `CustomAccount` class for `CustomProvider`.

    Find more documentation [HERE](https://petersimpson.dev/blog/django-allauth-custom-provider/)

    """
    pass


class CustomProvider(OAuth2Provider):

    """
    `CustomProvider` class to handle OAUTH2 authentication against a Geonode server.

    Find more documentation regarding custom provider setup [HERE](https://petersimpson.dev/blog/django-allauth-custom-provider/)

    The Geonode server must have custom Django application `UserDetails` installed to expose required data.

    Find more documentation regarding custom Django application `UserDetails` [HERE](https://github.com/phardy-egis/django-geonode-userdetails.git)

    """

    id = 'oauthtoolkitprovider'
    name = 'oauthtoolkitprovider'
    account_class = CustomAccount

    def extract_uid(self, data):
        logger.debug('OAUTH2 (user ID): {data}'.format(data=str(data)))
        return str(data['id'])

    def extract_common_fields(self, data):
        logger.debug('OAUTH2 (data): {data}'.format(data=str(data)))
        if data['auth']:
            return dict(username=data['username'], first_name=data['username'], last_name=data['username'],)
        else:
            return None

    def get_default_scope(self):
        scope = ['write']
        return scope


providers.registry.register(CustomProvider)