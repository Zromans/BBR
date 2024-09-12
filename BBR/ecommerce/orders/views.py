from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem, ShippingOption
from .forms import ShippingAddressForm
from cart.cart import Cart
import uuid

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                order_number=generate_order_number(),
                total_amount=cart.get_total_price(),
                shipping_address=form.cleaned_data['shipping_address'],
                billing_address=form.cleaned_data['billing_address']
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            cart.clear()
            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingAddressForm()
    
    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

def generate_order_number():
    return str(uuid.uuid4()).split('-')[0].upper()

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # TODO: Implement actual payment gateway integration
    payment_successful = True  # Placeholder, always successful
    if payment_successful:
        order.status = 'processing'
        order.save()
        return True
    return False

def finalize_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if process_payment(request, order_id):
        cart = Cart(request)
        cart.clear()
        
        order.confirmation_number = f"ORD-{order.id:06d}"
        order.save()
        
        send_order_confirmation_email(order)
        send_order_notification_to_admin(order)
        
        return redirect('order_confirmation', order_id=order.id)
    else:
        messages.error(request, 'Payment processing failed. Please try again.')
        return redirect('payment_failed')

def send_order_confirmation_email(order):
    subject = f'Order Confirmation - {order.order_number}'
    message = f'Thank you for your order. Your order number is {order.order_number}.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])

def send_order_notification_to_admin(order):
    subject = f'New Order - {order.order_number}'
    message = f'A new order has been placed. Order number: {order.order_number}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

def order_review(request):
    cart = Cart(request)
    shipping_options = ShippingOption.objects.all()
    
    if request.method == 'POST':
        shipping_option_id = request.POST.get('shipping_option')
        shipping_option = get_object_or_404(ShippingOption, id=shipping_option_id)
        
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.get_total_price() + shipping_option.price,
            shipping_option=shipping_option,
            status='pending'
        )
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
        
        return redirect('process_payment', order_id=order.id)
    
    return render(request, 'orders/review.html', {
        'cart': cart,
        'shipping_options': shipping_options,
    })

def apply_coupon(request):
    # TODO: Implement coupon validation and application
    pass

def guest_checkout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})
        if created:
            user.set_unusable_password()
            user.save()
        
        login(request, user)
        return redirect('order_review')
    
    return render(request, 'orders/guest_checkout.html')

def payment_failed(request):
    return render(request, 'orders/payment_failed.html')

def track_checkout_step(request, step):
    # TODO: Implement actual analytics tracking
    print(f"User {request.user.id} reached checkout step: {step}")
