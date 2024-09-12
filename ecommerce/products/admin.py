from django.contrib import admin
from .models import Category, Product, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'movement_type', 'reason', 'timestamp']
    list_filter = ['movement_type', 'timestamp']
