from django.apps import AppConfig

class ScrapingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraping'

    def ready(self):
        from .scraper import run_scraper, import_scraped_data
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def run_scraper_and_import(sender, **kwargs):
            if sender.name == 'scraping':
                # Run the scraper and import the scraped data
                scraped_data = run_scraper()
                import_scraped_data(scraped_data)

