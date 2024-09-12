from django.db import models
from django.contrib.auth.models import User

class SavedCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

# In cart/cart.py
def save_cart_for_user(self, user):
    SavedCart.objects.update_or_create(
        user=user,
        defaults={'cart_data': self.cart}
    )

def load_cart_for_user(self, user):
    try:
        saved_cart = SavedCart.objects.get(user=user)
        self.cart = saved_cart.cart_data
        self.save()
    except SavedCart.DoesNotExist:
        pass
