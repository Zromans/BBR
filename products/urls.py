from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('start-scrape/', views.start_scrape, name='start_scrape'),
    path('get-models/', views.get_models, name='get_models'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('filter/', views.filter_products, name='filter_products'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('product/<int:product_id>/submit-review/', views.submit_review, name='submit_review'),
]
