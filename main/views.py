from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Item, Order, Table
from .forms import *
from django.forms import formset_factory
import queue
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test

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


@user_passes_test(lambda u: u.is_staff, login_url='login')
def order(request):
    order = Order.objects.all()
    return render(request, "main/order.html", {'order': order})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def orders(request, pk):
    table = Table.objects.filter(id=pk).first()
    orderformset = formset_factory(OrderForm)
    formset = orderformset(request.POST or None)
    if formset.is_valid():
        for form in formset:
            order = form.save(commit=False)
            order.table = table
            order.save()
        return redirect('/order')

    return render(request, 'main/orders.html', {'formset': formset, 'table': table})


@permission_required('is_superuser', raise_exception=True)
def allorders(request):
    high = Order.objects.all().filter(item__time__range=(0, 4))
    medium = Order.objects.all().filter(item__time__range=(5, 8))
    low = Order.objects.all().filter(item__time__range=(9, 13))
    q1 = queue.Queue()
    q1.put(high)
    q2 = queue.Queue()
    q2.put(medium)
    q3 = queue.Queue()
    q3.put(low)
    q1 = q1.get()
    q2 = q2.get()
    q3 = q3.get()
    context = {
        'high': q1,
        'medium': q2,
        'low': q3,
    }
    return render(request, 'main/allorder.html', context)


@permission_required('is_superuser', raise_exception=True)
def onallorders(request):
    high = OnOrder.objects.all().filter(item__time__range=(0, 4))
    medium = OnOrder.objects.all().filter(item__time__range=(5, 8))
    low = OnOrder.objects.all().filter(item__time__range=(9, 13))
    q1 = queue.Queue()
    q1.put(high)
    q2 = queue.Queue()
    q2.put(medium)
    q3 = queue.Queue()
    q3.put(low)
    q1 = q1.get()
    q2 = q2.get()
    q3 = q3.get()

    context = {
        'high': q1,
        'medium': q2,
        'low': q3,
    }
    return render(request, 'main/on_allorder.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='login')
def tables(request):
    tables = Table.objects.all()
    return render(request, 'main/tables.html', {'tables': tables})


@permission_required('is_superuser', raise_exception=True)
def prepare(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        if order.status == 'pending...':
            order.status = "preparing..."
        else:
            order.status = "prepared"
        order.save()
        return redirect('/allorders')

    return render(request, 'main/prepare.html', {'order': order})


@login_required(login_url='login')
def on_orders(request):
    orderformset = formset_factory(OnOrderForm)
    formset = orderformset(request.POST or None)
    if formset.is_valid():
        for form in formset:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
        return redirect('/')

    return render(request, 'main/on_orders.html', {'formset': formset})


@login_required(login_url='login')
def on_order(request, user):
    order = OnOrder.objects.filter(user=request.user)
    return render(request, "main/on_order.html", {'order': order})


@permission_required('is_superuser', raise_exception=True)
def on_prepare(request, pk):
    order = get_object_or_404(OnOrder, pk=pk)

    if request.method == 'POST':
        if order.status == 'pending...':
            order.status = "preparing..."
        else:
            order.status = "prepared"
        order.save()
        return redirect('/on_allorders')

    return render(request, 'main/on_prepare.html', {'order': order})

