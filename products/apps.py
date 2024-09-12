from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from django.apps import apps
        from django.contrib import admin

        app_models = apps.get_app_config('products').get_models()
        for model in app_models:
            admin.site.register(model)
