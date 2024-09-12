import csv
import requests
from bs4 import BeautifulSoup
from .models import Year, Make, Model, Product
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import cv2

class Command(BaseCommand):
    help = 'Scrape products from the specified website using machine learning and AI techniques'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ml_model = None
        self.vectorizer = None

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Base URL of the website to scrape')
        parser.add_argument('--pages', type=int, default=10, help='Number of pages to scrape')
        parser.add_argument('--delay', type=int, default=1, help='Delay between requests in seconds')
        parser.add_argument('--output', type=str, default='scraped_products.csv', help='Output CSV file name')
        parser.add_argument('--email', action='store_true', help='Send email notification when scraping is complete')
        parser.add_argument('--model', type=str, default='model.pkl', help='Path to the trained machine learning model')
        parser.add_argument('--vectorizer', type=str, default='vectorizer.pkl', help='Path to the trained vectorizer')

    def handle(self, *args, **options):
        base_url = options['url']
        num_pages = options['pages']
        delay = options['delay']
        output_file = options['output']
        send_email = options['email']
        model_path = options['model']
        vectorizer_path = options['vectorizer']

        self.stdout.write(self.style.SUCCESS(f'Starting scraping from {base_url}'))

        self.load_ml_model(model_path, vectorizer_path)

        scraped_data = self.scrape_products(base_url, num_pages, delay)

        if scraped_data:
            self.stdout.write(self.style.SUCCESS(f'Scraped {len(scraped_data)} products'))
            csv_file = self.save_to_csv(scraped_data, output_file)
            self.stdout.write(self.style.SUCCESS(f'Scraped data saved to {csv_file}'))

            if send_email:
                self.send_email_notification(csv_file)
        else:
            self.stdout.write(self.style.WARNING('No products found'))

    def load_ml_model(self, model_path, vectorizer_path):
        with open(model_path, 'rb') as file:
            self.ml_model = pickle.load(file)
        with open(vectorizer_path, 'rb') as file:
            self.vectorizer = pickle.load(file)

    def scrape_products(self, base_url, num_pages, delay):
        scraped_data = []

        for page in range(1, num_pages + 1):
            url = f'{base_url}?page={page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            products = self.identify_products(soup)

            for product in products:
                name = self.extract_text(product, 'product-name')
                price = self.extract_price(product)
                year_str = self.extract_text(product, 'year')
                make_str = self.extract_text(product, 'make')
                model_str = self.extract_text(product, 'model')
                image_url = self.extract_image_url(product)

                year, _ = Year.objects.get_or_create(year=int(year_str))
                make, _ = Make.objects.get_or_create(name=make_str)
                model, _ = Model.objects.get_or_create(name=model_str, make=make)

                product, created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        'price': price,
                        'image': image_url,
                    }
                )

                product.years.add(year)
                product.makes.add(make)
                product.product_models.add(model)

                scraped_data.append({
                    'name': name,
                    'price': price,
                    'year': year_str,
                    'make': make_str,
                    'model': model_str,
                    'image_url': image_url
                })

            self.stdout.write(self.style.SUCCESS(f'Scraped page {page} of {num_pages}'))
            time.sleep(delay)

        return scraped_data

    def identify_products(self, soup):
        products = []
        for element in soup.find_all():
            text = element.get_text(strip=True)
            if self.predict_product(text):
                products.append(element)
        return products

    def predict_product(self, text):
        if self.ml_model is None or self.vectorizer is None:
            raise ValueError('Machine learning model or vectorizer not loaded')

        text_vector = self.vectorizer.transform([text])
        prediction = self.ml_model.predict(text_vector)
        return prediction[0]

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
            fieldnames = ['name', 'price', 'year', 'make', 'model', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return filename

    def send_email_notification(self, csv_file):
        subject = 'Product Scraping Complete'
        message = f'The product scraping process has completed. The scraped data is attached as {csv_file}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]
        attachments = [csv_file]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False, attachments=attachments)
        self.stdout.write(self.style.SUCCESS('Email notification sent'))

