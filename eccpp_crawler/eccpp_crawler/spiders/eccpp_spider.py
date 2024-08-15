import scrapy
from urllib.parse import urljoin

class EccppSpiderSpider(scrapy.Spider):
    name = "eccpp_spider"
    allowed_domains = ["eccppautoparts.com"]
    start_urls = ["https://eccppautoparts.com"]

    def parse(self, response):
        # Extract all links
        links = response.css('a::attr(href)').getall()
        
        for link in links:
            absolute_url = urljoin(response.url, link)
            
            # If it's a product page, parse it
            if '/product/' in absolute_url:
                yield scrapy.Request(absolute_url, callback=self.parse_product)
            else:
                # If it's not a product page, follow the link
                yield scrapy.Request(absolute_url, callback=self.parse)

    def parse_product(self, response):
        # Extract product information
        name = response.css('h1.product-title::text').get()
        price = response.css('span.price::text').get()
        sku = response.css('span.sku::text').get()

        # Extract product specifics
        specifics = {}
        specifics_rows = response.css('div.product-specifics tr')
        for row in specifics_rows:
            key = row.css('th::text').get()
            value = row.css('td::text').get()
            if key and value:
                specifics[key.strip(':')] = value.strip()

        # Extract includes
        includes = response.css('div.product-includes li::text').getall()

        yield {
            'url': response.url,
            'name': name,
            'price': price,
            'sku': sku,
            'specifics': specifics,
            'includes': includes
        }