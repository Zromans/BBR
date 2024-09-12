from django.contrib import admin
from products.models import Product, Category, Year, Make, Model
from orders.models import Order, OrderItem
from scraping.models import ScrapedData

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Year)
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ScrapedData)

