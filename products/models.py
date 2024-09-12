from django.db import models

class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class Make(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='models')

    class Meta:
        unique_together = ('name', 'make')

    def __str__(self):
        return f"{self.make} {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    years = models.ManyToManyField(Year, related_name='products')
    makes = models.ManyToManyField(Make, related_name='products')
    models = models.ManyToManyField(Model, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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