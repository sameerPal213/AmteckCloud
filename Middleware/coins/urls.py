# vim: ai ts=4 sts=4 et sw=4

from django.urls import path
from . import views

app_name = "coins"
urlpatterns = [
        path('api/jobs/', views.JobList.as_view(), name='job-list'),
        path('api/sections/', views.SectionList.as_view(), name='section-list'),
        path('api/activities/', views.ActivityList.as_view(), name='activity-list'),
        # ex. /coins/job/
        path('job/', views.JobIndexView.as_view(), name="index"),
        # ex. /coins/job/1/
        path('job/<int:pk>/', views.DetailView.as_view(), name='job_detail'),
        # ex. /coins/job/1000013/pos/
        path('job/<str:job_num>/pos/', views.job_test, name='job_test'),
        # ex. /coins/project/ 
        #   POST - updates box folder structure
        path('projects/', views.projects, name='Projects'),
        # ex. /coins/poline/
        path('poline/', views.poline, name='PO Line'),
        path('', views.JobIndexView.as_view(), name="index")
        ]
