import csv
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Make, Model, Product, Category, Review
from .scraper import scrape_products
from django.core.paginator import Paginator

def home(request):
    return render(request, 'products/home.html')

def start_scrape(request):
    # ... (existing code remains the same)

def get_models(request):
    # ... (existing code remains the same)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def search_products(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'products/search_results.html', {'products': products, 'query': query})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

def filter_products(request):
    # Retrieve filter parameters from the request
    brand = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    # Apply filters to the products queryset
    products = Product.objects.all()
    if brand:
        products = products.filter(brand=brand)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    return render(request, 'products/filter_results.html', {'products': products})

def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'products/product_reviews.html', {'product': product, 'reviews': reviews})

def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Retrieve review data from the request
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Create a new review object and save it
        review = Review(product=product, rating=rating, comment=comment)
        review.save()
        
        return redirect('products:product_detail', product_id=product.id)
    
    return render(request, 'products/submit_review.html', {'product': product})