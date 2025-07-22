import ldap3
import os
from django.core.management.base import BaseCommand
from dotenv import load_dotenv, find_dotenv

class Command(BaseCommand):
    help = 'Explore LDAP users'

    def handle(self, *args, **kwargs):
        # Load environment variables
        load_dotenv(find_dotenv())

        # LDAP server and credentials
        server_uri = os.environ['LDAP_SERVER_URI']
        bind_dn = "CN=AMT WebApp LDAP,OU=AMT Service Accounts,OU=Region 02 Service Accounts,OU=Operating Location Service Accounts,OU=Privileged Service Accounts,OU=IT Team,DC=cs,DC=loc"
        bind_password = os.environ['LDAP_PASSWORD']
        search_base = "ou=amt users,ou=region 02 users,ou=operating location users,ou=operating locations,dc=cs,dc=loc"
        search_filter = "(&(objectClass=user)(proxyAddresses=smtp:mervin@amteck.com))"

        # Connect to the LDAP server
        server = ldap3.Server(server_uri)
        conn = ldap3.Connection(server, bind_dn, bind_password, auto_bind=True)

        # Search for a user
        conn.search(search_base, search_filter, attributes=ldap3.ALL_ATTRIBUTES)

        # Print the attributes of the first user found
        if conn.entries:
            user = conn.entries[0]
            self.stdout.write(self.style.SUCCESS(user.entry_to_json()))

        conn.unbind()