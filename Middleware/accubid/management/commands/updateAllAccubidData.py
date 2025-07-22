from datetime import datetime
import sys
import json
import requests
import webbrowser
from django.core.management.base import BaseCommand
from accubid.models import Database, Project, Estimate
from am_nexus.settings import ACCUBID_BASE_URL, APP_NAME, CLIENT_ID, CLIENT_SECRET, CODE_CHALLENGE, CODE_VERIFIER, TRIMBLE_BASE_URL

class Command(BaseCommand):
    help = 'Updates all Accubid data'
    code = None
    access_token = None

    def add_arguments(self, parser):
        parser.add_argument('--access-token', dest='access_token', help='Access token for API authentication')

    def handle(self, *args, **options):
        self.access_token = options.get('access_token')

        if not self.access_token:
            params = {
                'client_id': CLIENT_ID,
                'response_type': 'code',
                'scope': f'openid {APP_NAME}',
                'redirect_uri': 'http://127.0.0.1/',
                'code_challenge': CODE_CHALLENGE,
                'code_challenge_method': 'S256'
            }
            url = f'{TRIMBLE_BASE_URL}/oauth/authorize'
            response = requests.get(url, params=params)
            # open the browser to the response url
            webbrowser.open(response.url)
            # get the returned code from the user
            self.code = input("Enter the code: ")

            # Make a POST request to obtain the access token
            token_url = f'{TRIMBLE_BASE_URL}/oauth/token'
            data = {
                'grant_type': 'authorization_code',
                'code': self.code,
                'code_verifier': CODE_VERIFIER,
                'tenantDomain': 'Trimble.com',
                'redirect_uri': 'http://127.0.0.1/',
                'client_id': CLIENT_ID
            }
            response = requests.post(token_url, auth=(CLIENT_ID, CLIENT_SECRET), data=data)
            # Handle the response
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')

                # Get the databases
                self.getDatabases()
            else:
                print(response.json())
                print("Failed to obtain access token")
        else:
            # Get the databases
            self.getDatabases()

    def convert_date(self, value):
        """
        Converts a date value to a Python date object.

        Args:
            value: The date value to be converted.

        Returns:
            The converted Python date object.

        Raises:
            ValueError: If no valid date format is found.
        """
        if value:
            for format in ('%m/%d/%y', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%m/%d/%Y', ):
                try:
                    return datetime.strptime(str(value), format).date()
                except ValueError:
                    pass
            raise ValueError('no valid date format found')
        else:
            return None

    def getEstimates(self, projectId, databaseToken):
        url = f'{ACCUBID_BASE_URL}/estimate/v1/estimates/{databaseToken}/{projectId}'
        # Make a GET request to retrieve the estimates
        response = requests.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        # Handle the response
        if response.status_code == 200:
            estimates = response.json()
            for estimate in estimates:
                createdDate = self.convert_date(estimate['CreatedDate'])
                dueDate = self.convert_date(estimate['DueDate'])
                startDate = self.convert_date(estimate['StartDate'])
                endDate = self.convert_date(estimate['EndDate'])

                estimate_object, created = Estimate.objects.get_or_create(
                    id=estimate['EstimateID'],
                    defaults={
                        "name": estimate["EstimateName"],
                        'number': estimate['EstimateNumber'],
                        'status': estimate['Status'].lower(),
                        'createdDate': createdDate,
                        'dueDate': dueDate,
                        'startDate': startDate,
                        'endDate': endDate,
                        'contract': estimate['Contract'],
                        'isDeleted': estimate['IsDeleted']
                    })
                print(f'Estimate Name: {estimate_object.name} Created: {created}')
        else:
            print(response.json())
            print("Failed to retrieve estimates")

    def getProjects(self, databaseToken):
        url = f'{ACCUBID_BASE_URL}/project/v1/projects/{databaseToken}'
        # Make a GET request to retrieve the projects
        response = requests.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        # Handle the response
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                startDate = self.convert_date(project['StartDate'])
                endDate = self.convert_date(project['EndDate'])
                createdDate = self.convert_date(project['CreatedDate'])

                project_object, created = Project.objects.get_or_create(
                    id=project['ProjectID'],
                    defaults={
                        "name": project["ProjectName"],
                        'number': project['ProjectNumber'],
                        'type': project['Type'],
                        'startDate': startDate,
                        'endDate': endDate,
                        'createdDate': createdDate,
                        'managingBranchName': project['ManagingBranchName'],
                        'projectPath': project['ProjectPath'],
                        'trimbleProjectId': project['TrimbleProjectID']
                    })
                print(f'Project Name: {project_object.name} Created: {created}')
                self.getEstimates(project_object.id, databaseToken)
            # Process the projects
            # ...
        else:
            print(response.json())
            print("Failed to retrieve projects")

    def getDatabases(self):
        url = f'{ACCUBID_BASE_URL}/database/v1/databases'
        # Make a GET request to retrieve the databases
        response = requests.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        if response.status_code == 200:
            databases = response.json()
            for database in databases:
                # Check if the database already exists
                database_object, created = Database.objects.get_or_create(
                    token=database['Token'],
                    defaults={
                        "name": database["DatabaseName"],
                        'company': database['CompanyName']
                    })
                self.getProjects(database_object.token)
        else:
            print(response.json())
            print("Failed to retrieve databases")
