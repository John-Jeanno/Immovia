from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('', views.bail_list, name='bail_list'),
    path('creer/', views.creer_bail, name='creer_bail'),
]
