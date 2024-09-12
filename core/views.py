from django.shortcuts import render
from products.models import Product
from orders.models import Order, OrderItem



def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    total_orders = Order.objects.count()
    context = {
        'latest_products': latest_products,
        'total_orders': total_orders,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
