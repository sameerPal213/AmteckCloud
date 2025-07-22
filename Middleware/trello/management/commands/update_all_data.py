from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.db import models
from django.db.models import Count
from trello.resources import WorkspaceResource
from trello.models import Workspace, Board
import requests
import tablib
import json
from tqdm import tqdm


mapping_dict = {
        'Workspace': {
            'trello_id':    'id',
            'enterprise':   'idEnterprise',
            'name':         'name',
            'display_name': 'displayName',
            'description':  'desc',
            'url':          'url'
            },
        'Board': {
            'id':               'trello_id',
            'idOrganization':   'workspace',
            'name':             'name',
            'desc':             'description',
            'descData':         'desc_data',
            'closed':           'closed',
            'pinned':           'pinned',
            'url':              'url',
            'shortUrl':         'short_url'
            },
        'List': {
            'id':       'trello_id',
            'idBoard':  'board',
            'name':     'name'
            }
        }
"""
The logic of this command is the following:
    1) Starting with the Enterprise, pull a list of all the Workspaces under it.
        - This one has to be done manually to start the program but the logic
          from here is modular and runs recursively
    2) For each Workspace, go over all fields and try to update, if the field is
        a foreign key, recursively do the same. This should therefore catch all
        direct inheritance objects
"""


class Command(BaseCommand):
    help = """
        Pull all current Trello data and update any out of date records or 
        create any missing records."""
    boards_url = ('https://api.trello.com/1/organizations/{workspace_id}'
                    '/boards?filter=open&fields=id,idOrganization,name,'
                    'desc,closed,url,shortUrl')
    enterprise_id = '62cf3c59215ba6781190769f'

    def handle(self, *args, **options):
        # checks that the trello api token and key are set
        if not settings.TRELLO_TOKEN or not settings.TRELLO_KEY:
            self.stdout.write(self.style.ERROR(
                "API key or token is missing. Check your .env file.")
                )
            return
        # starts the loop by getting all Workspaces of the Enterprise
        self.get_children(
            self.enterprise_id, 
            'Enterprise', 
            (
                f'enterprises/{self.enterprise_id}'
                '?organizations=members'
                '&organization_fields=id,name,displayName,desc,url'
            ),
            'Workspace')

    def get_children(self, parent_id, parent_model_name, children_endpoint,
            child_model_name):
        full_url = "https://api.trello.com/1/" + children_endpoint
        params = {
                "key": settings.TRELLO_KEY,
                "token": settings.TRELLO_TOKEN
            }

        try:
            # make the call
            response = requests.get(full_url, params)
            response.raise_for_status()
            children = response.json()
            # enterprises list their children differently
            if parent_model_name == 'Enterprise':
                children = children['organizations']

            # compare children with database and update as needed
            with transaction.atomic():
                resource = WorkspaceResource()
                dataset = tablib.Dataset()
                children = json.load(children)
                dataset.load(json.load(children), format='json')
                result = resource.import_data(dataset, dry_run=False)
                for child in tqdm(
                        children,
                        desc=( f'Updating {child_model_name}s for '
                                f'{parent_model_name} {parent_id}'),
                        leave=False):
                    return

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.ERROR(
                f'Error fetching {child_model_name}s from Trello'))
