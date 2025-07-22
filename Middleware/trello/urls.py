# trello/urls.py

from django.urls import path
from . import views

urlpatterns = [
        path('action/', views.action, name='action'),
        path('action/<str:modeltype>/', views.action),
        path('action/<str:modeltype>/<str:modelid>/', views.action),
        path('form/', views.sample_form, name='sample_form'),
        path('', views.index, name='index'),
]
