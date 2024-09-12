from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('filter/', views.filter_products, name='filter_products'),
    path('reviews/<int:product_id>/', views.product_reviews, name='product_reviews'),
    path('submit-review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('flash-sales/', views.flash_sales, name='flash_sales'),
    path('start-scrape/', views.start_scrape, name='start_scrape'),
    path('start-ftp-import/', views.start_ftp_import, name='start_ftp_import'),
    path('get-models/', views.get_models, name='get_models'),
    path('import-ftp/', views.import_ftp_view, name='import_ftp'),
]