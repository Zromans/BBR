from django.contrib import admin
from .models import Make, Model, Year, Category, Product

class MakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')
    list_filter = ('make',)
    search_fields = ('name',)

class YearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    search_fields = ('year',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'price', 'year', 'make', 'model', 'category')
    list_filter = ('make', 'model', 'year', 'category')
    search_fields = ('name', 'part_number')
    autocomplete_fields = ('make', 'model', 'year', 'category')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'part_number', 'price', 'description', 'image')
        }),
        ('Categorization', {
            'fields': ('make', 'model', 'year', 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Make, MakeAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
