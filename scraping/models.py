from django.db import models

class ScrapedData(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)
    fitments = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    manufacturer_part_number = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    placement = models.CharField(max_length=100, blank=True)
    surface_finish = models.CharField(max_length=100, blank=True)
    warranty = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    load_bearing = models.CharField(max_length=100, blank=True)
    includes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.sku}"

    @classmethod
    def import_data(cls, data):
        """
        Import scraped data into the database.
        """
        for item in data:
            cls.objects.update_or_create(
                url=item['url'],
                defaults={
                    'name': item['name'],
                    'price': item['price'],
                    'sku': item['sku'],
                    'fitments': item.get('fitments', ''),
                    'brand': item.get('brand', ''),
                    'manufacturer_part_number': item.get('manufacturer_part_number', ''),
                    'type': item.get('type', ''),
                    'placement': item.get('placement', ''),
                    'surface_finish': item.get('surface_finish', ''),
                    'warranty': item.get('warranty', ''),
                    'material': item.get('material', ''),
                    'load_bearing': item.get('load_bearing', ''),
                    'includes': item.get('includes', ''),
                }
            )

