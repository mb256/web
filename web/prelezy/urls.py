from django.urls import path
from . import views

app_name = 'prelezy'

urlpatterns = [
    path('', views.prelezy, name='prelezy'),
    path('data/', views.prelezy_data, name='prelezy_data'),
]
