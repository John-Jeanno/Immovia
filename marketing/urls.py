from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('', views.campagne_list, name='campagne_list'),
    path('creer/', views.creer_campagne, name='creer_campagne'),
]
