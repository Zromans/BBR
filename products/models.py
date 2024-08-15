from django.db import models

class Make(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make.name} {self.name}"

class Year(models.Model):
    value = models.IntegerField()
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model} {self.value}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.name}"