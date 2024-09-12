import json
import logging
from decimal import Decimal
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .models import ScrapedData
from .config import ECCPP_PRODUCTS_FILE
from .spiders.eccpp_spider import EccppSpiderSpider

logger = logging.getLogger(__name__)

def run_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EccppSpiderSpider)
    process.start()

def import_scraped_data():
    try:
        with open(ECCPP_PRODUCTS_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"Scraped data file not found: {ECCPP_PRODUCTS_FILE}")
        return

    cleaned_data = []
    for item in data:
        try:
            cleaned_item = {
                'url': item['url'],
                'name': item['name'],
                'price': Decimal(item['price'].replace('$', '')),
                'sku': item['sku'],
                'fitments': item.get('fitments', ''),
                'brand': item.get('brand', ''),
                'manufacturer_part_number': item.get('manufacturer_part_number', ''),
                'type': item.get('type', ''),
                'placement': item.get('placement', ''),
                'surface_finish': item.get('surface_finish', ''),
                'warranty': item.get('warranty', ''),
                'material': item.get('material', ''),
                'load_bearing': item.get('load_bearing', ''),
                'includes': item.get('includes', ''),
            }
            cleaned_data.append(cleaned_item)
        except (KeyError, ValueError) as e:
            logger.error(f"Error cleaning data: {e}")
            continue

    ScrapedData.objects.bulk_create(
        [ScrapedData(**item) for item in cleaned_data],
        ignore_conflicts=True
    )
    logger.info(f"Imported {len(cleaned_data)} products into the database.")

def run_scraper_and_import():
    run_scraper()
    import_scraped_data()
