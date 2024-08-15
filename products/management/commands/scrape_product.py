from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.eccpp_spider import EccppSpiderSpider
from products.models import Product
import json

class Command(BaseCommand):
    help = 'Scrape products from eccppautoparts.com'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(EccppSpiderSpider)
        process.start()

        # After scraping, read the JSON file and import to database
        try:
            with open('products.json', 'r') as f:
                products = json.load(f)
            
            for product in products:
                Product.objects.create(
                    name=product['name'],
                    price=product['price'],
                    sku=product['sku'],
                    # Add other fields as necessary
                )
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} products'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('No products were scraped. The JSON file was not created.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error reading the JSON file. It may be empty or invalid.'))



After making these changes, try running the command again:

python manage.py scrape_product



This updated version should handle the login process more robustly and provide more information about what's happening during the scraping process. If you're still encountering issues, please provide the new output and any error messages you receive.

Try again with different context
Add context...
Avatar for zachary.romans-qvpvn
from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings

from scraper.spiders.product_spider import ProductSpider

from products.models import Product

import json

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time



class Command(BaseCommand):

    help = 'Scrape products from eccppautoparts.com'



    def handle(self, *args, **options):

        # Set up Selenium

        chrome_options = Options()

        chrome_options.add_argument("--headless")  # Run in headless mode

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



            email_field.send_keys("your_email@example.com")  # Replace with actual email

            password_field.send_keys("your_password")  # Replace with actual password

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

                    products = json.load(f)

                

                for product in products:

                    Product.objects.create(

                        name=product['name'],

                        price=product['price'],

                        # Add other fields as necessary

                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} products'))

            except FileNotFoundError:

                self.stdout.write(self.style.ERROR('No products were scraped. The JSON file was not created.'))

            except json.JSONDecodeError:

                self.stdout.write(self.style.ERROR('Error reading the JSON file. It may be empty or invalid.'))



        finally:

            driver.quit()  is what is currently written


Thank you for providing the current content of your scrape_product.py file. This setup looks good as it combines Selenium for handling the login process and Scrapy for the actual scraping. Let's make a few adjustments to improve it:

Update the login credentials.
Add more error handling and logging.
Ensure the Scrapy spider is properly configured to use the Selenium driver.
Here's the updated scrape_product.py:

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.product_spider import ProductSpider
from products.models import Product
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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

            email_field.send_keys("zachary@bbrparts.com")  # Use actual email
            password_field.send_keys("@Rion62177")  # Use actual password
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
                    products = json.load(f)
                
                for product in products:
                    Product.objects.create(
                        name=product['name'],
                        price=product['price'],
                        sku=product.get('sku', ''),  # Add SKU field
                        # Add other fields as necessary
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} products'))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR('No products were scraped. The JSON file was not created.'))
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Error reading the JSON file. It may be empty or invalid.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))

        finally:
            driver.quit()