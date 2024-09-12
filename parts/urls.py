from django.urls import path
from . import views

app_name = 'parts'

urlpatterns = [
    path('', views.parts_list, name='list'),
    path('search/', views.parts_search, name='search'),
    path('filter/', views.parts_filter, name='filter'),
    path('<int:pk>/', views.parts_detail, name='detail'),
    path('make/<str:make_name>/', views.parts_by_make, name='by_make'),
    path('model/<str:model_name>/', views.parts_by_model, name='by_model'),
    path('year/<int:year>/', views.parts_by_year, name='by_year'),
    path('category/<str:category_name>/', views.parts_by_category, name='by_category'),
]