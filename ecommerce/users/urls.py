from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_history, name='user_order_history'),
]