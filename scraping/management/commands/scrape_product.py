import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraping.spiders.eccpp_spider import EccppSpiderSpider
from products.models import Product, Make, Model, Year, Category
import json
import logging

class Command(BaseCommand):
    help = 'Scrape products and categories from eccppautoparts.com'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        process = CrawlerProcess(get_project_settings())
        process.crawl(EccppSpiderSpider)
        process.start()

        try:
            with open('products.json', 'r') as f:
                items = json.load(f)
            
            if not items:
                logger.warning("No items were scraped. The JSON file is empty.")
                return

            for item in items:
                # Adjust this part based on the actual structure of your scraped data
                Product.objects.create(
                    name=item['name'],
                    price=float(item['price'].replace('$', '').replace(',', '')),
                    sku=item['sku'],
                    url=item['url']
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(items)} items'))
        except FileNotFoundError:
            logger.error('No items were scraped. The JSON file was not created.')
        except json.JSONDecodeError:
            logger.error('Error reading the JSON file. It may be empty or invalid.')
        except Exception as e:
            logger.error(f'An error occurred: {str(e)}')