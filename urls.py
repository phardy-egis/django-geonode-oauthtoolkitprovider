from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import OAuthToolkitProvider

urlpatterns = default_urlpatterns(OAuthToolkitProvider)