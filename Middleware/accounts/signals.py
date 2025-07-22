# accounts/signals.py
from django.conf import settings
from django.contrib.auth.models import Group
from django_auth_ldap.backend import populate_user
from django.dispatch import receiver


@receiver(populate_user)
def sync_ldap_groups(sender, user, ldap_user, **kwargs):
    # Ensure the user instanc is saved before modifying groups
    if not user.pk:
        user.save()
    # Clear existing groups
    user.groups.clear()

    # Get the LDAP group names
    ldap_groups = ldap_user.group_names

    # Map LDAP groups to Django groups
    for ldap_group in ldap_groups:
        django_group, created = Group.objects.get_or_create(name=ldap_group)
        user.groups.add(django_group)