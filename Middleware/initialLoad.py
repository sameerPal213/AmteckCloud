import requests
from django.conf import settings

def create_webhooks(url, memberId):
    member_boards_url = f"https://api.trello.com/1/members/{memberId}/organizations"
    org_boards_url = "https:/api.trello.com/1/organizations/{id}/boards"
    webhook_url = "https://api.trello.com/1/webhooks/?callbackURL={callbackURL}&idModel={idModel}"

    # Make a GET request to get a list of organizations the member is a part of
    params = {
            'key': settings.TRELLO_KEY,
            'token': settings.TRELLO_TOKEN
            }
    member_organizations_response = requests.get(member_boards_url, params=params)
    print(member_organizations_response)
