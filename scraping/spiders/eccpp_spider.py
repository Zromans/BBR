import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class EccppSpiderSpider(scrapy.Spider):
    name = "eccpp_spider"
    allowed_domains = ["eccppautoparts.com"]
    login_url = "https://eccppautoparts.com/account/login"
    start_urls = ["https://eccppautoparts.com"]

    def __init__(self, *args, **kwargs):
        super(EccppSpiderSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        self.driver.get(self.login_url)
        
        # Wait for the email input field to be present
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "customer[email]"))
        )
        email_input.send_keys("zachary@bbrparts.com")
        
        password_input = self.driver.find_element(By.NAME, "customer[password]")
        password_input.send_keys("@Rion62177")
        
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        login_button.click()
        
        # Wait for login to complete
        time.sleep(5)
        
        if "My Account" in self.driver.page_source:
            self.logger.info("Login successful")
            yield scrapy.Request(self.start_urls[0], callback=self.parse_categories, dont_filter=True)
        else:
            self.logger.error("Login failed")

    def parse_categories(self, response):
        self.driver.get(response.url)
        
        # Wait for category links to be present
        category_links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.category-link"))
        )
        
        for link in category_links:
            category_url = link.get_attribute('href')
            yield scrapy.Request(category_url, callback=self.parse_category, dont_filter=True)

    def parse_category(self, response):
        self.driver.get(response.url)
        
        # Wait for product links to be present
        product_links = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.product-link"))
        )
        
        for link in product_links:
            product_url = link.get_attribute('href')
            yield scrapy.Request(product_url, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        self.driver.get(response.url)
        
        # Wait for product details to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-title"))
        )
        
        yield {
            'name': self.driver.find_element(By.CSS_SELECTOR, "h1.product-title").text,
            'price': self.driver.find_element(By.CSS_SELECTOR, "span.price").text,
            'sku': self.driver.find_element(By.CSS_SELECTOR, "span.sku").text,
            'url': response.url
        }

    def closed(self, reason):
        self.driver.quit()
        self.logger.info(f"Spider closed: {reason}")
