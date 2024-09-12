import csv
import aiohttp
import asyncio
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import cv2
import pandas as pd
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import concurrent.futures
from ratelimit import limits, sleep_and_retry
from .models import Product, Year, Make, Model
from django.core.files.base import ContentFile
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler('scraper.log')
    logger.addHandler(file_handler)

setup_logging()

class Command(BaseCommand):
    help = 'Scrape products from the specified website using machine learning and AI techniques'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Base URL of the website to scrape')
        parser.add_argument('--pages', type=int, default=10, help='Number of pages to scrape')
        parser.add_argument('--delay', type=int, default=1, help='Delay between requests in seconds')
        parser.add_argument('--output', type=str, default='scraped_products.csv', help='Output CSV file name')
        parser.add_argument('--email', action='store_true', help='Send email notification when scraping is complete')
        parser.add_argument('--model', type=str, default='model.pkl', help='Path to the trained machine learning model')
        parser.add_argument('--vectorizer', type=str, default='vectorizer.pkl', help='Path to the trained vectorizer')

    def handle(self, *args, **options):
        self.start_time = timezone.now()
        base_url = options['url']
        num_pages = options['pages']
        delay = options['delay']
        output_file = options['output']
        send_email = options['email']
        model_path = options['model']
        vectorizer_path = options['vectorizer']

        logger.info(f'Starting scraping from {base_url}')

        self.load_ml_model(model_path, vectorizer_path)

        scraped_data = asyncio.run(self.scrape_products(base_url, num_pages, delay))

        if scraped_data:
            logger.info(f'Scraped {len(scraped_data)} products')
            csv_file = self.save_to_csv(scraped_data, output_file)
            logger.info(f'Scraped data saved to {csv_file}')

            if send_email:
                self.send_email_notification(csv_file)
        else:
            logger.warning('No products found')

        self.log_scraping_duration()

    def load_ml_model(self, model_path, vectorizer_path):
        with open(model_path, 'rb') as file:
            self.ml_model = pickle.load(file)
        with open(vectorizer_path, 'rb') as file:
            self.vectorizer = pickle.load(file)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def scrape_page(self, session, url):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def scrape_products(self, base_url, num_pages, delay):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in range(1, num_pages + 1):
                url = f'{base_url}?page={page}'
                tasks.append(asyncio.create_task(self.scrape_page(session, url)))
                await asyncio.sleep(delay)
            
            pages_content = await asyncio.gather(*tasks)
            
            scraped_data = []
            for content in pages_content:
                products = self.identify_products(content)
                for product in products:
                    scraped_data.append(self.extract_product_data(product))
            
            return scraped_data

    def identify_products(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        product_elements = soup.find_all('div', class_='product-item')
        
        identified_products = []
        for element in product_elements:
            text = element.get_text(strip=True)
            if self.predict_product(text):
                identified_products.append(element)
        
        return identified_products

    def predict_product(self, text):
        if self.ml_model is None or self.vectorizer is None:
            raise ValueError('Machine learning model or vectorizer not loaded')

        text_vector = self.vectorizer.transform([text])
        prediction = self.ml_model.predict(text_vector)
        return prediction[0]

    def extract_product_data(self, product):
        name = self.extract_text(product, 'product-name')
        price = self.extract_price(product)
        year_str = self.extract_text(product, 'year')
        make_str = self.extract_text(product, 'make')
        model_str = self.extract_text(product, 'model')
        image_url = self.extract_image_url(product)
        description = self.extract_text(product, 'product-description')
        sku = self.extract_text(product, 'product-sku')
        stock = self.extract_text(product, 'product-stock')
        category = self.extract_text(product, 'product-category')

        return {
            'name': name,
            'price': price,
            'year': year_str,
            'make': make_str,
            'model': model_str,
            'image_url': image_url,
            'description': description,
            'sku': sku,
            'stock': stock,
            'category': category,
            'scraped_at': timezone.now(),
        }

    def extract_text(self, element, class_name):
        text_element = element.find(class_=class_name)
        if text_element:
            return text_element.get_text(strip=True)
        return ''

    def extract_price(self, element):
        price_element = element.find(class_='price')
        if price_element:
            price_text = price_element.get_text(strip=True)
            return float(price_text.replace('$', '').replace(',', ''))
        return 0.0

    def extract_image_url(self, element):
        image_element = element.find('img')
        if image_element and 'src' in image_element.attrs:
            return image_element['src']
        return ''

    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'price', 'year', 'make', 'model', 'image_url', 'description', 'sku', 'stock', 'category', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return filename

    def send_email_notification(self, csv_file):
        subject = 'Product Scraping Complete'
        message = f'The product scraping process has completed. The scraped data is saved as {csv_file}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        logger.info('Email notification sent')

    def log_scraping_duration(self):
        if self.start_time:
            duration = timezone.now() - self.start_time
            logger.info(f'Total scraping duration: {duration}')

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        file_name = default_storage.save(csv_file.name, csv_file)
        file_path = default_storage.path(file_name)
        
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            product = Product(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                sku=row['sku'],
                stock=row['stock'],
                category=row['category'],
                scraped_at=timezone.now(),
            )
            if 'image_path' in row:
                img = cv2.imread(row['image_path'])
                img_resized = cv2.resize(img, (300, 300))
                _, buffer = cv2.imencode('.jpg', img_resized)
                content = ContentFile(buffer.tobytes())
                product.image.save(f"{product.pk}.jpg", content, save=True)
            product.save()
        
        return JsonResponse({'message': 'CSV uploaded and processed successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def train_ml_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
    grid_search = GridSearchCV(SVC(), param_grid, cv=5)
    grid_search.fit(X_train_vectorized, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)
    
    logger.info(f"Model Accuracy: {accuracy}")
    
    return best_model, vectorizer

def preprocess_data(data):
    return np.array(data)

def feature_engineering(data):
    return np.hstack([data, np.log1p(data)])

class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = proxies
        self.current = 0

    def get_proxy(self):
        proxy = self.proxies[self.current]
        self.current = (self.current + 1) % len(self.proxies)
        return proxy

proxy_rotator = ProxyRotator(['http://proxy1.com', 'http://proxy2.com'])

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def scrape_with_proxy(url):
    try:
        response = requests.get(url, proxies={'http': proxy_rotator.get_proxy()})
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error scraping {url}: {str(e)}")
        raise

def import_scraped_data(self):
    # Implement the logic to import scraped data
    # For example:
    with open(self.options['output'], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Product.objects.create(
                name=row['name'],
                description=row['description'],
                price=float(row['price']),
                sku=row['sku'],
                stock=int(row['stock']),
                category=row['category']
            )
