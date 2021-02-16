from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('table', 'status',)

# class TableForm(forms.ModelForm):
#     table_set = Table.objects.all()
#     table = forms.ModelChoiceField(queryset=table_set, empty_label=Table, required=True)
#
#     class Meta:
#         model = Table
#         fields = ['table']
