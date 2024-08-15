from django.contrib import admin
from .models import Make, Model, Year, Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'price', 'year', 'make', 'model', 'category')
    list_filter = ('make', 'model', 'year', 'category')
    search_fields = ('name', 'part_number')

admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Year)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)