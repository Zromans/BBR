from django.core.management.base import BaseCommand
from scraping.scraper import run_scraper

class Command(BaseCommand):
    help = 'Runs the web scraper'

    def handle(self, *args, **options):
        run_scraper()
        self.stdout.write(self.style.SUCCESS('Successfully ran scraper'))