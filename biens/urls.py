from django.urls import path
from . import views

app_name = 'biens'

urlpatterns = [
    path('', views.liste_biens, name='liste_biens'),
    path('ajouter/', views.ajouter_bien, name='ajouter_bien'),
]
