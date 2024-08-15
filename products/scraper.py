import csv
import requests
from bs4 import BeautifulSoup
from .models import Year, Make, Model, Product
import time

def scrape_products():
    base_url = 'https://example.com/cars/'  # Replace with the actual URL
    scraped_data = []

    for page in range(1, 10):  # Adjust the range based on the number of pages
        url = f'{base_url}?page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', class_='product-item')  # Adjust based on actual HTML structure
        
        for product in products:
            name = product.find('h2', class_='product-name').text.strip()
            price = float(product.find('span', class_='price').text.strip().replace('$', '').replace(',', ''))
            year_str = product.find('span', class_='year').text.strip()
            make_str = product.find('span', class_='make').text.strip()
            model_str = product.find('span', class_='model').text.strip()
            image_url = product.find('img', class_='product-image')['src']
            
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
        
        time.sleep(1)

    return scraped_data

def save_to_csv(data, filename='scraped_products.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'price', 'year', 'make', 'model', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return filename



