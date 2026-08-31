from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.index, name='list'),
    path('nouveau/', views.create, name='create'),
]
