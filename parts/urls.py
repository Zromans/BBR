from django.urls import path
from . import views

app_name = 'parts'

urlpatterns = [
    path('', views.parts_list, name='list'),
]