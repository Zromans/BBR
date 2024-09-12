from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category
from django.apps import apps

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    app_config = apps.get_app_config('products')
    for category_name in app_config.dynamic_categories:
        Category.objects.get_or_create(name=category_name)

@receiver(post_migrate)
def update_categories(sender, **kwargs):
    app_config = apps.get_app_config('products')
    existing_categories = set(Category.objects.values_list('name', flat=True))
    new_categories = set(app_config.dynamic_categories) - existing_categories
    
    for category_name in new_categories:
        Category.objects.create(name=category_name)
