from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ScrapingConfig(AppConfig):
    name = 'scraping'

    def ready(self):
        from .scraper import run_scraper_and_import
        post_migrate.connect(self.run_scraper_on_migrate, sender=self)

    def run_scraper_on_migrate(self, sender, **kwargs):
        from .scraper import run_scraper_and_import
        run_scraper_and_import()

def run_scraper_and_import(sender, **kwargs):
    if sender.name == 'scraping':
        from .scraper import run_scraper, import_scraped_data
        scraped_data = run_scraper()
        import_scraped_data(scraped_data)
        update_product_catalog()

def update_product_catalog():
    from .models import ScrapedData
    from products.models import Product
    scraped_items = ScrapedData.objects.all()
    for item in scraped_items:
        Product.objects.update_or_create(
            sku=item.sku,
            defaults={
                'name': item.name,
                'price': item.price,
                'description': item.description,
                'last_updated': item.last_updated
            }
        )

def clean_old_data():
    from django.utils import timezone
    from .models import ScrapedData
    threshold = timezone.now() - timezone.timedelta(days=30)
    old_data = ScrapedData.objects.filter(last_updated__lt=threshold)
    old_data.delete()

def run_scheduled_tasks():
    run_scraper_and_import(ScrapingConfig)
    clean_old_data()
