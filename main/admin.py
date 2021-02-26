from django.contrib import admin
from .models import Category, Item, Order, Table, OnOrder

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(OnOrder)
