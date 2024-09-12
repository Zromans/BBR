from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from .models import Product, StockMovement

@user_passes_test(lambda u: u.is_staff)
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        reason = request.POST.get('reason')
        movement_type = 'in' if quantity > 0 else 'out'

        try:
            StockMovement.objects.create(
                product=product,
                quantity=abs(quantity),
                movement_type=movement_type,
                reason=reason
            )
            messages.success(request, f"Stock updated successfully. New stock: {product.stock}")
        except ValidationError as e:
            messages.error(request, str(e))

    return redirect('product_detail', slug=product.slug)
