from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.account.signals import user_logged_in
import logging
# from .utils import sync_groups
from django.contrib.auth.models import Group
from geonode.groups.models import GroupProfile, GroupMember
from slugify import slugify

logger = logging.getLogger("django")

class OAuthToolkitAccount(ProviderAccount):
    pass

class OAuthToolkitProvider(OAuth2Provider):

    id = 'oauthtoolkitprovider'
    name = 'oauthtoolkitprovider'
    account_class = OAuthToolkitAccount
    pkce_enabled_default = True

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):  
        # storing roles in session variable to sync roles after log in
        self.request.session["synced_roles"] = {"values":data['roles']}
        return dict(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )


    def get_default_scope(self):
        scope = ['read']
        return scope

def sync_user_groups_after_login(sender, user, request, **kwargs):
    from geonode.people.models import Profile
    user = Profile.objects.get(id=user.id)

    # Adding user to its active roles
    user_groups = []
    for role in request.session["synced_roles"]["values"]:
        # Creating group in geonode
        group, created = GroupProfile.objects.get_or_create(slug=slugify(role), defaults={'title':role, 'access':'private'})           
        group.join(user)
        user_groups.append(group)
    
    # Remove user membership from unused roles
    groupsmembers_to_remove = GroupMember.objects.exclude(group__in=user_groups).filter(user=user).distinct()
    for groupsmember_to_remove in groupsmembers_to_remove:
        groupsmember_to_remove.group.leave(user)
        

user_logged_in.connect(sync_user_groups_after_login)
providers.registry.register(OAuthToolkitProvider)