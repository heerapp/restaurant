from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('table', 'status',)


class OnOrderForm(forms.ModelForm):
    class Meta:
        model = OnOrder
        exclude = ('user', 'status', )