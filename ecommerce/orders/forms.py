from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(required=True)

    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address', 'agree_to_terms']
