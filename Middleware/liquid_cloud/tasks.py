# liquid_cloud/tasks.py
from celery import shared_task
import requests
import pyodata
from django.conf import settings

@shared_task
def pull_database_information():
    # Initiate request data
    officeNumber = 842
    odata_url = f'https://liquidcloudserver.comfortsystemsusa.com/odata/v1/OfficeNumber/GenericItemsByOfficeNumber(officeNumber={officeNumber})'

    # User NTLM authentication
    username = settings.WINDOWS_USERNAME
    password = settings.WINDOWS_PASSWORD
    session = requests.Session()
    session.auth = (username, password)

    response = pyodata.Client(odata_url, session)

    if response.status_code == 200:
        data = response.json()
        print(data[0])
    else:
        print(f"Failed to fetch data: {response.status_code}")
