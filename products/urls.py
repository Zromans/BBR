from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('order-history/', views.order_history, name='order_history'),
    path('flash-sales/', views.flash_sales, name='flash_sales'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('product-share/<int:product_id>/', views.product_share, name='product_share'),
    path('contact/', views.contact, name='contact'),
    path('start-scrape/', views.start_scrape, name='start_scrape'),
    path('import-ftp/', views.import_ftp_view, name='import_ftp'),
]