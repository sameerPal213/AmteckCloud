# trello/tasks.py

import pyodbc
import json
from am_nexus.celery import app
from celery.utils.log import get_task_logger
from datetime import datetime
from django.conf import settings
from .models import (
	Action, Member, Webhook, Card, List, Board, Workspace, CustomField, Label,
	Checklist, CheckItem, CustomFieldItem, MissingAction, CustomFieldOption, 
	Enterprise, Comment)
from .utils import getDataFromTrello, updateEnterprise

logger = get_task_logger(__name__)


@app.task(bind=True)
def delayPrint(self, inStr):
	print(inStr)


# This is the function that writes the data to the database
@app.task(bind=True)
def insertAction(self, jsonData):
	try:
		# log the action type
		action_type = jsonData['action']['type']
		logger.info(f'Action Type: {action_type}.')

		# get the creator value
		try: 
			creator = jsonData['action']['appCreator']['name']
		except: 
			creator = ''
		# convert date string
		datetime_object = datetime.strptime(
			jsonData['action']['date'], 
			"%Y-%m-%dT%H:%M:%S.%fZ")
		formatted_date = datetime_object.strftime("%Y-%m-%d")

		# create the action record
		action = Action(
			trello_id   = jsonData['action']['id'],
			data        = json.dumps(jsonData['action']['data']),
			creator     = creator,
			type        = jsonData['action']['type'],
			date        = formatted_date,
			limits      = json.dumps(jsonData['action']['limits']),
			display     = json.dumps(jsonData['action']['display']))

		action.member, member_created = Member.objects.get_or_create(
				trello_id=jsonData['action']['idMemberCreator'],
				defaults={"username":"", "email":"", "full_name":""})

		action.webhook, webhook_created = Webhook.objects.get_or_create(
				trello_id=jsonData['webhook']['id'])

		action.save()

		# update the appropriate records based off the action
		routeAction(jsonData)

		# update items that were created
		if member_created:
			updateMember(action.member)
		if webhook_created:
			updateWebhook(action.webhook, "Member")

		return "Record processed successfully."
	except pyodbc.Error as e:
		logger.error(f"Data: {jsonData}")
		return f"Error: {e}"


def routeAction(jsonData):
	action_type = jsonData['action']['type']
	data        = jsonData['action']['data']
	key         = jsonData['action']['display']['translationKey']
	if action_type == "createCard":
		card = Card(trello_id=data['card']['id'])
		card.save()
		updateCard(card)
	elif action_type == "createCustomField":
		custom_field = CustomField(trello_id=data['customField']['id'])
		custom_field.save()
		updateCustomField(custom_field)
	elif action_type == "createLabel":
		label = Label(trello_id=data['label']['id'])
		label.save()
		updateLabel(label)
	elif action_type == "addChecklistToCard":
		checklist = Checklist(trello_id=data['checklist']['id'])
		checklist.save()
		updateChecklist(checklist)
	elif action_type == "createCheckItem":
		check_item = CheckItem(trello_id=data['checkItem']['id'])
		check_item.save()
		updateCheckItem(check_item, data['checklist']['id'])
	elif action_type == "createList":
		list = List(trello_id=data['list']['id'])
		list.save()
		updateList(list)
	elif action_type == "addOrganizationToEnterprise":
		workspace = Workspace(trello_id=data['organization']['id'])
		workspace.save()
		updateWorkspace(workspace)
	elif action_type == "addToOrganizationBoard":
		board = Board(trello_id=data['board']['id'])
		board.save()
		updateBoard(board)
	# ManyToMany Relationships
	elif action_type == "addMemberToBoard":
		member, member_created  = Member.objects.get_or_create(
									trello_id=data['idMemberAdded'],
									defaults={"username":"", "email":"", "full_name":""})
		board, board_created    = Board.objects.get_or_create(
									trello_id=data['board']['id'],
									defaults={"name":"","short_url":""})
		board.members.add(member)
		# update if created
		if member_created:
			updateMember(member)
		if board_created:
			updateBoard(board)
	elif action_type == "removeMemberFromBoard":
		try:
			board   = Board.objects.get(trello_id=data['board']['id'])
			member  = Member.objects.get(trello_id=data['idMember'])
			board.members.remove(member)
		except Board.DoesNotExist:
			logger.info("Board doesn't exist")
		except Member.DoesNotExist:
			logger.info("Member doesn't exist")
	elif action_type == "addLabelToCard":
		label, label_created    = Label.objects.get_or_create(
									trello_id=data['label']['id'],
									defaults={"name":""})
		card, card_created      = Card.objects.get_or_create(
									trello_id=data['card']['id'])
		card.labels.add(label)
		# update if created
		if label_created:
			updateLabel(label)
		if card_created:
			updateCard(card)
	elif action_type == "removeLabelFromCard":
		try:
			card    = Card.objects.get(trello_id=data['card']['id'])
			label   = Label.objects.get(trello_id=data['label']['id'])
			card.labels.remove(label)
		except Card.DoesNotExist:
			logger.info("Card doesn't exist")
		except Label.DoesNotExist:
			logger.info("Label doesn't exist")
	elif action_type == "addMemberToCard":
		member, member_created  = Member.objects.get_or_create(
			trello_id=data['member']['id'],
			defaults={"username":"", "email":"", "full_name":""})
		card, card_created      = Card.objects.get_or_create(
			trello_id=data['card']['id'])
		card.members.add(member)
		# update if created
		if member_created:
			updateMember(member)
		if card_created:
			updateCard(card)
	elif action_type == "removeMemberFromCard":
		try:
			card    = Card.objects.get(trello_id=data['card']['id'])
			member  = Member.objects.get(trello_id=data['member']['id'])
			card.members.remove(member)
		except Card.DoesNotExist:
			logger.info("Card doesn't exist")
		except Member.DoesNotExist:
			logger.info("Member doesn't exist")
	elif action_type == "commentCard":
		comment = Comment(trello_id=jsonData['action']['id'])
		comment.save()
		updateComment(comment)
	elif action_type == "updateChecklist":
		checklist, checklist_created = Checklist.objects.get_or_create(
				trello_id=data['checklist']['id'])
		if key == "action_renamed_checklist":
			checklist.name = data['checklist']['name']
			checklist.save()
		# update if created
		if checklist_created:
			updateChecklist(checklist)
	elif action_type == "updateComment":
		comment, comment_created    = Comment.objects.get_or_create(
										trello_id=data['action']['id'])
		comment.text                = data['action']['text']
		comment.save()

		# update if created
		if comment_created:
			updateComment(comment)
	elif action_type == "updateList":
		list, list_created = List.objects.get_or_create(
			trello_id	= data['list']['id'],
			defaults	= {"name":""})
		if key == "action_archived_list":
			list.delete()
		elif key == "action_renamed_list":
			list.name = data['list']['name']
			list.save()
		# update if created
		if list_created:
			updateList(list)
	elif action_type == "updateCheckItem":
		check_item, check_item_created = CheckItem.objects.get_or_create(
				trello_id=data['checkItem']['id'])
		if key == "action_renamed_checkitem":
			check_item.name = data['checkItem']['name']
			check_item.save()
		# update if created
		if check_item_created:
			updateCheckItem(check_item, data['checklist']['id'])
	elif action_type == "updateCard":
		card, card_created = Card.objects.get_or_create(
				trello_id=data['card']['id'])
		if key == "action_archived_card":
			card.closed = 1
			card.save()
		elif key == "action_sent_card_to_board":
			card.closed = 0
			card.save()
		elif key == "action_changed_description_of_card":
			card.description = data['card']['desc']
			card.save()
		elif key == "action_added_a_due_date":
			card.due = data['card']['due']
			card.save()
		elif key == "action_added_a_start_date":
			card.start = data['card']['start']
			card.save()
		elif key == "action_renamed_card":
			card.name = data['card']['name']
			card.save()
		elif key == "action_move_card_from_list_to_list":
			list, list_created = List.objects.get_or_create(
				trello_id	= data['listAfter']['id'],
				defaults	= {"name":""})
			card.list = list
			if list_created:
				updateList(list)
		else:
			missing_action = MissingAction(
					data=json.dumps(data),
					display=json.dumps(jsonData['action']['display']),
					type=action_type)
			missing_action.save()
			
		# update if created
		if card_created:
			updateCard(card)
	elif action_type == "updateOrganization":
		workspace, workspace_created = Workspace.objects.get_or_create(
			trello_id	= data['organization']['id'],
			defaults	= {
				"name": "",
				"display_name": "",
				"description": ""})
		if key == "action_changed_description_of_organization":
			workspace.description = data['organization']['desc']
			workspace.save()
		elif key == "action_changed_display_name_of_organization":
			workspace.display_name = data['organization']['displayName']
			workspace.save()
		elif key == "action_changed_website_of_organization":
			workspace.url = data['organization']['url']
			workspace.save()
		# update if created
		if workspace_created:
			updateWorkspace(workspace)
	elif action_type == "updateBoard":
		board, board_created = Board.objects.get_or_create(
			trello_id=data['board']['id'],
			defaults={"name":"","short_url":""})
		if key == "action_update_board_name":
			board.name = data['board']['name']
			board.save()
		elif key == "action_update_board_desc":
			board.description = data['board']['desc']
			board.save()
		elif key == "action_closed_board":
			board.closed = 1
			board.save()
		elif key == "action_reopened_board":
			board.closed = 0
			board.save()
		# update if created
		if board_created:
			updateBoard(board)
	elif action_type == "updateCheckItemStateOnCard":
		check_item, check_item_created = CheckItem.objects.get_or_create(
				trello_id=data['checkItem']['id'])
		check_item.state = data['checkItem']['state']
		check_item.save()
		# update if created
		if check_item_created:
			updateCheckItem(check_item, data['checklist']['id'])
	elif action_type == "updateCheckItemDue":
		check_item, check_item_created  = CheckItem.objects.get_or_create(
											trello_id=data['checkItem']['id'])
		updateCheckItem(check_item, data['checklist']['id'])
	elif action_type == "updateLabel":
		label, label_created = Label.objects.get_or_create(
				trello_id=data['label']['id'],
				defaults={"name":""})
		if key == "unknown":
			label.name  = data['label']['name']
			label.color = data['label']['color']
			label.board, board_created = Board.objects.get_or_create(
				trello_id=data['board']['id'],
				defaults={"name":"","short_url":""})
			# update if created
			if board_created:
				updateBoard(label.board)
		# updte if created
		if label_created:
			updateLabel(label)
	elif action_type == "updateCustomField":
		custom_field, custom_field_created = CustomField.objects.get_or_create(
				trello_id=data['customField']['id'])
		if key == "action_rename_custom_field":
			custom_field.name = data['customField']['name']
			custom_field.save()
		# update if created
		if custom_field_created:
			updateCustomField(custom_field)
	elif action_type == "updateCustomFieldItem":
		cfi, cfi_created = CustomFieldItem.objects.get_or_create(
				trello_id       = data['customFieldItem']['id'])
		cfi.card, card_created = Card.objects.get_or_create(
				trello_id       = data['card']['id'])
		cfi.custom_field, cf_created = CustomField.objects.get_or_create(
				trello_id       = data['customField']['id'])
		if data['customFieldItem']['idValue'] is not None:
			cfi.customFieldOption, cfo_created = CustomFieldOption.objects.get_or_create(
					trello_id       = data['customFieldItem']['idValue'])
		cfi.value               = json.dumps(data['customFieldItem']['value'])
		# update if created
		if card_created:
			updateCard(cfi.card)
		if cf_created:
			updateCustomField(cfi.custom_field)
		#if cfi_created:                        # I don't think this is needed
		#    updateCustomFieldItem(cfi)         # the above should work
	elif action_type == "removeFromOrganizationBoard":
		try:
			board = Board.objects.get(trello_id=data['board']['id'])
			board.delete()
		except Board.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "deleteCheckItem":
		try:
			checkItem = CheckItem.objects.get(trello_id=data['checkItem']['id'])
			checkItem.delete()
		except CheckItem.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "removeChecklistFromCard":
		try:
			checklist = Checklist.objects.get(trello_id=data['checklist']['id'])
			checklist.delete()
		except Checklist.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "deleteCard":
		try:
			card = Card.objects.get(trello_id=data['card']['id'])
			card.delete()
		except Card.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "deleteLabel":
		try:
			label = Label.objects.get(trello_id=data['label']['id'])
			label.delete()
		except Label.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "deleteCustomField":
		try: 
			custom_field = CustomField.objects.get(
					trello_id=data['customField']['id'])
			custom_field.delete()
		except CustomField.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e: 
			logger.error(f"Error: {e}")
	elif action_type == "deleteComment":
		try:
			comment = Comment.objects.get(
						trello_id=data['action']['id'])
			comment.delete()
		except Comment.DoesNotExist:
			logger.info("Item did not exist, no action needed")
		except Exception as e:
			logger.error(f"Error: {e}")
	else:
		missing_action = MissingAction(
				data=json.dumps(data),
				display=json.dumps(jsonData['action']['display']),
				type=action_type)
		missing_action.save()


def updateComment(comment):
	# get the information from trello
	data = getDataFromTrello(f"actions/{comment.trello_id}")

	# convert date string
	date = datetime.strptime(
		data['date'], 
		"%Y-%m-%dT%H:%M:%S.%fZ")

	# update fields
	comment.text                = data['data']['text']
	comment.card, card_created  = Card.objects.get_or_create(
									trello_id = data['data']['card']['id'])
	comment.date                = date
	comment.save()

	# update card if created
	if card_created:
		updateCard(comment.card)


def updateWebhook(webhook, type):
	# get the information from trello
	data = getDataFromTrello(f"webhooks/{webhook.trello_id}")

	# update fields
	webhook.description = data['description']
	webhook.model_id    = data['idModel']
	webhook.model_type  = type
	webhook.save()


def updateMember(member):
	# get the information from trello    
	data = getDataFromTrello(f"members/{member.trello_id}")

	# update fields
	member.enterprise, enterprise_created = Enterprise.objects.get_or_create(
		trello_id   = data['idEnterprise'],
		defaults	= {"name":""})
	member.username     = data['username']
	member.email        = str(data['email'] or '')
	member.full_name    = data['fullName']
	member.save()

	# update enterprise if new one is created
	if enterprise_created:
		updateEnterprise(member.enterprise)


def updateWorkspace(workspace):
	# get the information from trello
	data = getDataFromTrello(f"organizations/{workspace.trello_id}")

	# update fields
	workspace.name          = data['name']
	workspace.display_name  = data['displayName']
	workspace.description   = data['desc']
	workspace.url           = data['url']
	workspace.save()


def updateCheckItem(checkItem, checklistId):
	# get the information from trello
	data = getDataFromTrello(
			f"checklists/{checklistId}/checkItems/{checkItem.trello_id}")

	# convert date string
	try:
		due = datetime.strptime(
			data['due'],
			"%Y-%m-%dT%H:%M:%S.%fZ")
	except:
		due = None
		

	# update fields
	checkItem.checklist, checklist_created = Checklist.objects.get_or_create(
			trello_id   = checklistId)
	checkItem.name      = data['name']
	checkItem.complete  = data['state']
	checkItem.due       = due
	checkItem.save()

	# update checklist if new one is created
	if checklist_created:
		updateChecklist(checkItem.checklist)


def updateChecklist(checklist):
	# get the information from trello
	data = getDataFromTrello(f"checklists/{checklist.trello_id}")

	# update fields
	checklist.card, card_created = Card.objects.get_or_create(
			trello_id   = data['idCard'])
	checklist.name      = data['name']
	checklist.save()

	# update card if new one is created
	if card_created:
		updateCard(checklist.card)


def updateLabel(label):
	# get the information from trello
	data = getDataFromTrello(f"labels/{label.trello_id}")

	# update fields
	label.board, board_created = Board.objects.get_or_create(
		trello_id   = data['idBoard'],
		defaults={"name":"","short_url":""})
	label.name          = data['name']
	label.color         = data['color']
	label.save()

	# update board if new one is created
	if board_created:
		updateBoard(label.board)


def updateCustomField(customField):
	# get the information from trello
	data = getDataFromTrello(f"customFields/{customField.trello_id}")

	# update fields
	customField.board, board_created = Board.objects.get_or_create(
		trello_id   = data['idModel'],
		defaults={"name":"","short_url":""})
	customField.name   = data['name']
	customField.type   = data['type']
	customField.save()

	# update board if new one is created
	if board_created:
		updateBoard(customField.board)


def updateCard(card):
	# get the information from trello
	data = getDataFromTrello(f"cards/{card.trello_id}")

	# update fields
	card.board, board_created = Board.objects.get_or_create(
		trello_id   = data['idBoard'],
		defaults	={"name":"","short_url":""})
	card.list, list_created = List.objects.get_or_create(
		trello_id   = data['idList'],
		defaults	={"name":""})
	for labelId in data['idLabels']: # TODO need to check this and see why multipe labels are being returned even though "get or create" is being called
		label, label_created = Label.objects.get_or_create(
			trello_id=labelId,
			defaults={"name":""})
		card.labels.add(label)
		# update label if new one is created
		if label_created:
			updateLabel(label)

	card.closed         = data['closed']
	card.description    = data['desc']
	card.description_data = data['descData']
	card.due            = data['due']
	card.due_reminder   = data['dueReminder']
	card.email          = data['email']
	card.id_short       = data['idShort']
	card.id_attachment_cover = data['idAttachmentCover']
	card.name           = data['name']
	card.pos            = data['pos']
	card.short_link     = data['shortLink']
	card.short_url      = data['shortUrl']
	card.url            = data['url']
	card.cover          = json.dumps(data['cover'])
	card.start          = data['start']
	card.save()

	# get data for list or board if new 
	if list_created:
		updateList(card.list)
	if board_created:
		updateBoard(card.board)


def updateList(list):
	# get the information from trello
	data = getDataFromTrello(f"lists/{list.trello_id}")

	# update fields
	list.board, board_created = Board.objects.get_or_create(
		trello_id   = data['idBoard'],
		defaults={"name":"","short_url":""})
	list.name           = data['name']
	list.save()

	# update board if new one is created
	if board_created:
		updateBoard(list.board)


def updateBoard(board):
	# get the information from trello
	data = getDataFromTrello(f"boards/{board.trello_id}")

	# update fields
	board.workspace, workspace_created = Workspace.objects.get_or_create(
		trello_id   = data['idOrganization'],
		defaults	= {
			"name": "",
			"display_name": "",
			"description": ""})
	board.name          = data['name']
	board.description   = data['desc']
	board.desc_data     = data['descData']
	board.closed        = data['closed']
	board.pinned        = data['pinned']
	board.url           = data['url']
	board.short_url     = data['shortUrl']
	board.prefs         = json.dumps(data['prefs'])
	board.save()

	# update workspace if new one is created
	if workspace_created:
		updateWorkspace(board.workspace)
