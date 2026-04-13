from django.urls import path
from . import views

app_name = 'prelezy'

urlpatterns = [
    path('', views.prelezy, name='prelezy'),
]
