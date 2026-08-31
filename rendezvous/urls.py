from django.urls import path
from . import views

app_name = 'rendezvous'

urlpatterns = [
    path('', views.calendrier, name='calendrier'),
    path('creneau/creer/', views.creer_creneau, name='creer_creneau'),
]
