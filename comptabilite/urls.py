from django.urls import path
from . import views

app_name = 'comptabilite'

urlpatterns = [
    path('', views.tableau_bord, name='tableau_bord'),
    path('operation/ajouter/', views.creer_operation, name='creer_operation'),
]
