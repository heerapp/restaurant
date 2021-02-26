from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/")
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Table(models.Model):
    table = models.CharField(max_length=50)

    def __str__(self):
        return self.table


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100, default="pending...", blank=True)

    def __str__(self):
        return f"{self.item}"

    @property
    def price(self):
        price = self.item.price*self.quantity
        return price


class OnOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    status = models.CharField(max_length=100, default="pending...", blank=True)

    def __str__(self):
        return f"{self.user}"

    @property
    def price(self):
        price = self.item.price*self.quantity
        return price

