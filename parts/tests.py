from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Make, Model, Year, Category

class PartsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.make = Make.objects.create(name='Honda')
        self.model = Model.objects.create(name='Civic', make=self.make)
        self.year = Year.objects.create(year=2022)
        self.category = Category.objects.create(name='Engine')
        self.part = Product.objects.create(
            name='Engine Oil',
            description='High-quality engine oil',
            price=19.99,
            make=self.make,
            model=self.model,
            year=self.year,
            category=self.category
        )

    def test_parts_list_view(self):
        url = reverse('parts:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parts/parts_list.html')
        self.assertContains(response, self.part.name)

    def test_parts_detail_view(self):
        url = reverse('parts:detail', args=[self.part.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parts/parts_detail.html')
        self.assertContains(response, self.part.name)
        self.assertContains(response, self.part.description)

    # Add more test methods for other views and scenarios
