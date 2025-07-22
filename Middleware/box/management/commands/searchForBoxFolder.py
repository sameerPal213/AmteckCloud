import os
from django.core.management.base import BaseCommand
from boxsdk import JWTAuth, Client

class Command(BaseCommand):
    help = 'Search Box for a given search term in the folder name'

    def add_arguments(self, parser):
        parser.add_argument('search_term', type=str, help='The search term to look for in folder names')

    def handle(self, *args, **kwargs):
        search_term = kwargs['search_term']
        client = self.get_box_client()
        items = client.search().query(query=search_term, type='folder')

        if items:
            self.stdout.write(f'Folders found for search term "{search_term}":')
            for item in items:
                self.stdout.write(f'- {item.name} (ID: {item.id})')
        else:
            self.stdout.write(f'No folders found for search term "{search_term}".')

    def get_box_client(self):
        auth = JWTAuth.from_settings_file('./Middleware/box/config.json')
        client = Client(auth)
        usr = client.user(user_id='755000110')
        return client.as_user(usr)
