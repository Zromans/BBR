from .models import Make, Model, Year, Product
from django.urls import path
from django.db.models import Sum, Count
from django.contrib import admin
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import csv
from reversion.admin import VersionAdmin

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

@admin.register(Product)
class ProductAdmin(VersionAdmin):
    list_display = ['name', 'sku', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = ['category']
    search_fields = ['name', 'sku']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'sku', 'price', 'description', 'image')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    actions = ['mark_as_featured', 'update_stock', 'bulk_update_price', 'export_as_csv']

    change_list_template = 'admin/product_change_list.html'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)

    def update_stock(self, request, queryset):
        for product in queryset:
             product.stock += 10
        product.save()
        self.message_user(request, f"Stock updated for {queryset.count()} products.")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_dashboard),
            path('import-csv/', self.import_csv),
        ]
        return custom_urls + urls

    def admin_dashboard(self, request):
        context = {
            'total_products': Product.objects.count(),
            'total_value': Product.objects.aggregate(Sum('price'))['price__sum'],
            'products_by_category': Product.objects.values('category').annotate(count=Count('id')),
        }
        return render(request, 'admin/dashboard.html', context)

    def bulk_update_price(self, request, queryset):
        if 'apply' in request.POST:
            percentage = float(request.POST.get('percentage'))
            for product in queryset:
                product.price *= (1 + percentage / 100)
                product.save()
            self.message_user(request, f"Prices updated for {queryset.count()} products.")
            return HttpResponseRedirect(request.get_full_path())
        return render(request, 'admin/bulk_update_price.html', {'products': queryset})

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Part Number', 'Price', 'Year', 'Make', 'Model'])
        for product in queryset:
            writer.writerow([product.name, product.part_number, product.price, product.year, product.make, product.model])
        return response

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Product.objects.create(
                    name=row['Name'],
                    part_number=row['Part Number'],
                    price=float(row['Price']),
                    year=Year.objects.get_or_create(year=row['Year'])[0],
                    make=Make.objects.get_or_create(name=row['Make'])[0],
                    model=Model.objects.get_or_create(name=row['Model'], make=Make.objects.get(name=row['Make']))[0]
                )
            self.message_user(request, "CSV file imported successfully.")
            return redirect('..')
        return render(request, 'admin/csv_form.html')

admin.site.register(Make, MakeAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Year, YearAdmin)