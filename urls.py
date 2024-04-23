from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import CustomProvider
from django.urls import path, include
# from . import views
from rest_framework.routers import DefaultRouter

#
# Router
#
router = DefaultRouter()

#
# URLS
#

urlpatterns = default_urlpatterns(CustomProvider)
#urlpatterns += default_urlpatterns(AzureProvider)

urlpatterns += [
    # auth custom API endpoints
    path('', include(router.urls), name='oauthtoolkitprovider'),
]