from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Item, Order
from .forms import *


def index(request):
    category = Category.objects.all()
    item = Item.objects.all()

    context = {
        'category': category,
        'item': item,
    }
    return render(request, "main/index.html", context)


def item(request, pk):
    category = Category.objects.all()
    item = Item.objects.filter(category_id=pk)
    return render(request, "main/item.html", {'item': item, 'category': category})


def order(request):
    order = Order.objects.all()
    return render(request, "main/order.html", {'order': order})


def orders(request):
    form = OrderForm(request.POST or None)

    if form.is_valid():
        orders = form.save(commit=False)
        orders.save()
        return redirect('/')

    return render(request, 'main/orders.html', {'form': form})


def allorders(request):
    order = Order.objects.all()
    return render(request, 'main/allorder.html', {'order': order})



