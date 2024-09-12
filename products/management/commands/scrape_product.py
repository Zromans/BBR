from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .forms import CartAddProductForm
from products.models import Product, ProductDetail
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from django.conf import settings
from scraper.spiders.product_spider import ProductSpider

class Command(BaseCommand):
    help = 'Scrape products from eccppautoparts.com'

    def handle(self, *args, **options):
        # Set up Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the login page
            driver.get("https://eccppautoparts.com/account/login")

            # Wait for the login form to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CustomerEmail"))
            )

            # Fill in login details
            email_field = driver.find_element(By.ID, "CustomerEmail")
            password_field = driver.find_element(By.ID, "CustomerPassword")

            email_field.send_keys(settings.ECCPP_EMAIL)
            password_field.send_keys(settings.ECCPP_PASSWORD)
            password_field.send_keys(Keys.RETURN)

            # Wait for login to complete
            time.sleep(5)  # Adjust this delay as needed

            # Check if login was successful
            if "My Account" in driver.page_source:
                self.stdout.write(self.style.SUCCESS("Login successful"))
            else:
                self.stdout.write(self.style.ERROR("Login failed"))
                return

            # Now that we're logged in, start the Scrapy spider
            process = CrawlerProcess(get_project_settings())
            process.crawl(ProductSpider, driver=driver)
            process.start()

            # After scraping, read the JSON file and import to database
            try:
                with open('products.json', 'r') as f:
                    products_data = json.load(f)

                for product_data in products_data:
                    product, created = Product.objects.update_or_create(
                        sku=product_data['sku'],
                        defaults={
                            'name': product_data['name'],
                            'price': product_data['price'],
                            # Add other fields as necessary
                        }
                    )

                    # Create or update ProductDetail
                    ProductDetail.objects.update_or_create(
                        product=product,
                        defaults={
                            'description': product_data.get('description', ''),
                            'image_url': product_data.get('image_url', ''),
                            # Add other fields as necessary
                        }
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products_data)} products'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR('No products were scraped. The JSON file was not created.'))
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Error reading the JSON file. It may be empty or invalid.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

        finally:
            driver.quit()