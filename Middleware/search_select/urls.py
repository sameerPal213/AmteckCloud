from django.urls import path
from .views import ItemListView, item_form

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('form/', item_form, name='item-form'),
]
