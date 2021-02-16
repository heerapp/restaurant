from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Item, Order, Table
from .forms import *
from django.forms import formset_factory


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


def orders(request, pk):
    # table = TableForm(request.POST or None)
    table = Table.objects.filter(id=pk).first()
    orderformset = formset_factory(OrderForm)
    formset = orderformset(request.POST or None)
    if formset.is_valid():
        # Save table form and get table ID
        # a = table.save(commit=False)
        # a.save()

        for form in formset:
            order = form.save(commit=False)
            order.table = table
            order.save()
        return redirect('/order')

    return render(request, 'main/orders.html', {'formset': formset, 'table': table})


def allorders(request):
    high = Order.objects.all().filter(item__time__range=(0, 4))
    medium = Order.objects.all().filter(item__time__range=(5, 8))
    low = Order.objects.all().filter(item__time__range=(9, 13))

    context = {
        'high': high,
        'medium': medium,
        'low': low,
    }
    return render(request, 'main/allorder.html', context)


def tables(request):
    tables = Table.objects.all()
    return render(request, 'main/tables.html', {'tables': tables})


def prepare(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.status = "preparing..."
        order.save()
        return redirect('/allorders')

    return render(request, 'main/prepare.html', {'order': order})
