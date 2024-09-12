from django.test import TestCase
from django.urls import reverse
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=9.99,
            category=self.category
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'This is a test product')
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_category_list_view(self):
        response = self.client.get(reverse('products:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'products/category_list.html')

    def test_category_detail_view(self):
        response = self.client.get(reverse('products:category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/category_detail.html')

    def test_search_view(self):
        response = self.client.get(reverse('products:search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'products/search_results.html')

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)

    def test_remove_from_cart(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1})
        response = self.client.post(reverse('cart:remove_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(str(self.product.id), self.client.session['cart'])

    def test_checkout_process(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1})
        response = self.client.post(reverse('products:process_order'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'address': '123 Street, City'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/order_confirmation.html')
