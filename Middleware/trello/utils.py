from django.conf import settings
import requests
from trello.models import Enterprise


def updateEnterprise(enterprise):
	# get the information from trello
	data = getDataFromTrello(f"enterprises/{enterprise.trello_id}")

	# update fields
	enterprise.name = data['displayName']
	enterprise.save()


def getDataFromTrello(route):
	base_url    = "https://api.trello.com/1/"
	params      = {
		'token':    settings.TRELLO_TOKEN,
		'key':      settings.TRELLO_KEY
	}
	try:
		response = requests.get(base_url + route, params=params)
		response.raise_for_status()
	except requests.exceptions.RequestException as e:
		return {}
	return response.json()


def updateMember(db_member):
	enterprise_id = "62cf3c59215ba6781190769f"
	# get the information from trello
	data = getDataFromTrello(f"enterprise/{enterprise_id}/members/{db_member.trello_id}")

	# update fields
	db_member.enterprise, enterprise_created = Enterprise.objects.get_or_create(
		trello_id   = enterprise_id,
		defaults	= {"name":""})
	db_member.username     = data['username']
	db_member.full_name    = data['fullName']
	db_member.save()

	# update enterprise if new one is created
	if enterprise_created:
		updateEnterprise(db_member.enterprise)

	return db_member