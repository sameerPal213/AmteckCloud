# trello/views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import logging
from trello.tasks import insertAction
from trello.forms import SampleForm

logger = logging.getLogger(__name__)

# Handles any updates from trello
@csrf_exempt
def action (request, modeltype='', modelid=''):
    if request.method == "POST":
        try:
            # Convert call payload to dictionary
            requestJSON = json.loads(request.body)
            # This line dumps the request body if needed for debugging
            #logger.debug(json.dumps(requestJSON, indent=4))
            # pass to celery for async processing
            insertAction.delay(requestJSON)
            # Create the response for the api call
            response = {"Response": "Update has been submitted from processing"}
            return JsonResponse(response, status=200)
        # if processing the request doesn't work
        except:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    elif request.method == "HEAD":
        # return 200 so new webhooks can be created
        return JsonResponse({"Response": "Webhook endpoint online"}, status=200)

# Index Page
def index(request):
    return HttpResponse('Hello, welcome to the index page.')

# Form Testing
def sample_form(request):
    form = SampleForm()
    return render(request, "base.html", {"form": form})
