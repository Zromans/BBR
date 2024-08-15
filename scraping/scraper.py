import json
from decimal import Decimal
from .models import ScrapedData
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.eccpp_spider import EccppSpiderSpider

def scrape_and_import():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EccppSpiderSpider)
    process.start()

    # Check if the JSON file exists
    json_file_path = 'products.json'
    try:
        with open(json_file_path, 'r') as file:
            products = json.load(file)
    except FileNotFoundError:
        print("No products were scraped. The JSON file was not created.")
        return 0

    if not products:
        print("No products were found in the JSON file.")
        return 0

    for product in products:
        ScrapedData.objects.update_or_create(
            url=product['url'],
            defaults={
                'name': product['name'],
                'price': Decimal(product['price'].replace('$', '')) if product['price'] else Decimal('0.00'),
                'sku': product['sku'],
                'fitments': product['specifics'].get('Fitments', ''),
                'brand': product['specifics'].get('Brand', ''),
                'manufacturer_part_number': product['specifics'].get('Manufacturer Part Number', ''),
                'type': product['specifics'].get('Type', ''),
                'placement': product['specifics'].get('Placement on Vehicle', ''),
                'surface_finish': product['specifics'].get('Surface Finish', ''),
                'warranty': product['specifics'].get('Warranty', ''),
                'material': product['specifics'].get('Material', ''),
                'load_bearing': product['specifics'].get('Load Bearing', ''),
                'includes': '\n'.join(product['includes']),
            }
        )

    return len(products)