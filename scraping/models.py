from django.db import models

class ScrapedData(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)
    fitments = models.TextField()
    brand = models.CharField(max_length=100)
    manufacturer_part_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    placement = models.CharField(max_length=100)
    surface_finish = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    load_bearing = models.CharField(max_length=100)
    includes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sku}"  # Added closing parenthesis here