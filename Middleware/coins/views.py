# vim: ai ts=4 sts=4 et sw=4

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
import json
import logging
from .filters import JobFilter
from .models import Job, PurchaseOrder, Section, Activity
from .serializers import (
        JobSerializer, SectionSerializer, ActivitySerializer
        )
from .tasks import projectHandler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

logger = logging.getLogger(__name__)

"""This function receives a POST request at the 'projects' endpoint, extracts 
   the relevant data, and acknowledges the request as received"""
@csrf_exempt
def projects(req):
    #Handle request only if POST method
    if req.method == 'POST':
        #Create dictionary from byte stream
        byteStream = req.readlines()
        reqJSONStr = byteStream[0].decode('utf-8')
        print(reqJSONStr)
        reqJSON = json.loads(reqJSONStr)
        #Hand off dict to project handler
        projectHandler.apply_async(args=[reqJSON])
        #Format response and return to COINS
        resJSON = { 
        "Response": { 
            "ID": reqJSON["COINSInterface"]["Header"]["_attributes"]["id"]}}
        resJSONStr = json.dumps(resJSON)
        return HttpResponse(resJSONStr)


@csrf_exempt
def poline(req):
    # Handle request only if POST method
    if req.method == 'POST':
        # get the body and log to file
        requestJSON = json.loads(req.body)
        logger.debug(json.dumps(requestJSON, indent=4))

        response = {"Response": {"ID": requestJSON["COINSInterface"]["Header"]["_attributes"]["id"]}}
        return HttpResponse(response)


# VISIBLE WEBPAGES
class JobIndexView(LoginRequiredMixin, generic.ListView):
    model = Job
    paginate_by = 10
    template_name = "job/index.html"


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = "job/detail.html"


def job_pos(request, job_id):
    response = "You're looking at the POs of Job %s."
    return HttpResponse(response % job_id)


def job_test(request, job_num):
    job = get_object_or_404(Job, job_num=job_num)
    pos = get_list_or_404(PurchaseOrder, job_num=job_num)

    context = {"job": job, "pos": pos}
    
    if request.method == 'GET':
        return render(request, "job/detail.html", context)

# SERIALIZER VIEWS ############################################################# 
class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter


class SectionList(APIView):
    def get(self, request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityList(APIView):
    def get_queryset(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
