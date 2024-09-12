from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('<slug:slug>/edit/', views.edit_product, name='edit_product'),
    path('<slug:slug>/delete/', views.delete_product, name='delete_product'),
    path('<int:product_id>/update-stock/', views.update_stock, name='update_stock'),
]
