from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from django.db import transaction
from .models import Make, Model, Year, Product, Category, Review, Order, UserProfile, Cart, CartItem, ShippingOption, FlashSale
from .scraper import Command as ScraperCommand
from .forms import ProductSearchForm, ProductImportForm
import threading
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import stripe
import csv
import io
from stripe.error import StripeError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    featured_products = cache.get('featured_products')
    if not featured_products:
        featured_products = Product.objects.filter(featured=True)[:5]
        cache.set('featured_products', featured_products, 3600)  # Cache for 1 hour
    return render(request, 'products/home.html', {'featured_products': featured_products})

def start_scrape(request):
    if request.method == 'POST':
        threading.Thread(target=scrape_products_async).start()
        return JsonResponse({"message": "Scraping started"})
    return JsonResponse({"message": "Invalid request"}, status=400)

def scrape_products_async():
    scraper = ScraperCommand()
    options = {
        'url': 'https://example.com',  # Replace with your target URL
        'pages': 10,
        'delay': 1,
        'output': 'scraped_products.csv',
        'email': True,
        'model': 'model.pkl',
        'vectorizer': 'vectorizer.pkl'
    }
    scraper.handle(**options)

@transaction.atomic
def import_scraped_data(request):
    if request.method == 'POST':
        form = ProductImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            products = []
            for row in reader:
                product = {
                    'name': row['name'],
                    'description': row['description'],
                    'price': float(row['price']),
                    'sku': row['sku'],
                    'stock': int(row['stock']),
                    'category': row['category'],
                    'image_url': row.get('image_url', '')
                }
                products.append(product)
            
            return render(request, 'products/import_preview.html', {'products': products})
    else:
        form = ProductImportForm()
    
    return render(request, 'products/import_form.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product_id)[:4]
    return render(request, 'products/product_detail.html', {'product': product, 'related_products': related_products})

def search_products(request):
    query = request.GET.get('q', '')
    main_result = Product.objects.filter(name__icontains=query).first()
    related_results = Product.objects.filter(
        Q(category__icontains=query) |
        Q(description__icontains=query)
    ).exclude(id=main_result.id if main_result else None)[:5]

    context = {
        'query': query,
        'main_result': main_result,
        'related_results': related_results,
    }
    return render(request, 'search_results.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/category_detail.html', {'category': category, 'page_obj': page_obj})

def filter_products(request):
    products = Product.objects.all()
    brand = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    year = request.GET.get('year')
    make = request.GET.get('make')
    model = request.GET.get('model')
    
    if brand:
        products = products.filter(brand__icontains=brand)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if year:
        products = products.filter(year__year=year)
    if make:
        products = products.filter(make__name__icontains=make)
    if model:
        products = products.filter(model__name__icontains=model)
    
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/filter_results.html', {'page_obj': page_obj})

def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'products/product_reviews.html', {'product': product, 'reviews': reviews})

@transaction.atomic
def submit_review(request, product_id):
    if request.method == 'POST':
        review = Review(
            product_id=product_id,
            user=request.user,
            comment=request.POST['content'],
            rating=request.POST['rating'],
            created_at=timezone.now()
        )
        review.save()
        messages.success(request, 'Your review has been submitted successfully.')
    return redirect('products:product_detail', product_id=product_id)

def vote_review(request, review_id, vote_type):
    review = Review.objects.get(pk=review_id)
    if vote_type == 'helpful':
        review.helpful_votes += 1
    elif vote_type == 'not_helpful':
        review.not_helpful_votes += 1
    review.save()
    return redirect('products:product_detail', product_id=review.product.pk)

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request):
    if request.method == 'POST':
        token = request.POST['stripeToken']
        order = Order.objects.get(pk=request.POST['order_id'])
        
        try:
            stripe.Charge.create(
                amount=int(order.total_price * 100),  # amount in cents
                currency='usd',
                source=token,
                description=f'Order {order.pk}'
            )
            order.status = 'paid'
            order.save()
            return redirect('order_confirmation', order_id=order.pk)
        except StripeError as e:
            messages.error(request, f"Payment error: {str(e)}")
            return redirect('checkout')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Handle profile update
        profile.address = request.POST['address']
        profile.phone_number = request.POST['phone_number']
        profile.save()
        return redirect('user_profile')
    return render(request, 'products/user_profile.html', {'profile': profile})

def flash_sales(request):
    active_sales = FlashSale.objects.filter(
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now(),
        current_stock__gt=0
    )
    return render(request, 'flash_sales.html', {'active_sales': active_sales})

def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    shipping_options = ShippingOption.objects.all()
    return render(request, 'checkout.html', {'cart': cart, 'shipping_options': shipping_options})
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        question = request.POST.get('question')
        
        # Send email
        send_mail(
            subject=f"New contact from {name}",
            message=f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\nQuestion: {question}",
            from_email='your_email@example.com',
            recipient_list=['your_support_email@example.com'],
            fail_silently=False,
        )
        
        messages.success(request, "Your message has been sent. We'll get back to you soon!")
        return redirect('home')
    
    return render(request, 'contact.html')
