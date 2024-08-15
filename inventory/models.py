from django.db import models

class Scraping(models.Model):
    # Add fields as needed
    url = models.URLField(max_length=200)
    date_scraped = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)

class Make(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name