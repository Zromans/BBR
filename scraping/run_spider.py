from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.eccpp_spider import EccppSpiderSpider

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(EccppSpiderSpider)
    process.start()