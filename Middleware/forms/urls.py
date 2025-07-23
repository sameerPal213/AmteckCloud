# forms/urls.py
from django.urls import path
from forms import views

app_name = "forms"

# when a new request is received it tries each end point of this list in order
# and directs to the first matching example. When it matches it routes to the
# view provided
urlpatterns = [
        # API endpoints
        path('api/jsas/', views.SafetyTaskAnalysisResponseList.as_view(), name='sta-response-list'),
        # the form entry screen
        path('qaqc/100_1/new/', views.qaqc100_1, name="100_1-new"),
        # Downloads the pdf of the response
        path('qaqc/100_1/<int:response_id>/', views.create_qaqc_100_1_pdf, name='pdf-view'),
        # List of responses to form
        path('qaqc/100_1/', views.QAQC100_1IndexView.as_view(), name='QAQC Form 100.1'),
        # list of available QAQC forms
        path('qaqc/', views.qaqc_forms_index, name='QAQC Index'),
        path('jsa/', views.STAResponseList.as_view(), name='staresponse-list'),
        # entry screen for this form
        path('jsa/new/', views.jsa_entry, name='new-jsa-form'),
        # downloads the pdf of the response
        path('jsa/<str:jsa_box_id>/', views.view_jsa_pdf, name='view-jsa-pdf'),
        path('jsa/<int:response_id>/post-task/', views.post_task_assignment, name='post-task-assignment'),
        path('', views.forms_home_page, name='forms-home'),

        path('amq/100_1/new/', views.amq100_1, name="amq_100_1-new"),
        path('amq/100_2/new/', views.amq100_2, name="amq_100_2-new"),
        ]
