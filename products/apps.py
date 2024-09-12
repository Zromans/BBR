from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    dynamic_categories = []

    def ready(self):
        from django.apps import apps
        from django.contrib import admin
        from .signals import create_default_categories, update_categories

        app_models = apps.get_app_config('products').get_models()
        for model in app_models:
            if not admin.site.is_registered(model):
                admin.site.register(model)

        # Connect the signals
        post_migrate.connect(create_default_categories, sender=self)
        post_migrate.connect(update_categories, sender=self)

        # Perform app initialization
        self.initialize_app()

    def initialize_app(self):
        self.load_dynamic_categories()

    def load_dynamic_categories(self):
        if hasattr(settings, 'DYNAMIC_CATEGORIES'):
            self.dynamic_categories = settings.DYNAMIC_CATEGORIES
        else:
            # Fallback to database or default categories
            from .models import Category
            self.dynamic_categories = list(Category.objects.values_list('name', flat=True))

        if not self.dynamic_categories:
            self.dynamic_categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden']
