from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Item, Order, Table, CartItems
from .forms import *
from django.forms import formset_factory
import queue
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

process_list = []
result_list = []


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
    order1 = Order.objects.all().filter(table__table="t1")
    order2 = Order.objects.all().filter(table__table="t2")
    order3 = Order.objects.all().filter(table__table="t3")
    order4 = Order.objects.all().filter(table__table="t4")
    order5 = Order.objects.all().filter(table__table="t5")
    context = {
        "order1": order1,
        "order2": order2,
        "order3": order3,
        "order4": order4,
        "order5": order5
    }
    return render(request, "main/order.html", context)


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
            new_process_name = order.item
            new_process_at = 1
            new_process_st = order.item.time

            new_process = Process(new_process_name, new_process_at, new_process_st)
            if new_process_name is not None:
                process_list.append(new_process)
        return redirect('/result-page')
    result_list.clear()

    return render(request, 'main/orders.html', {'formset': formset, 'table': table})


@permission_required('is_superuser', raise_exception=True)
def allorders(request):
    high = Order.objects.all().filter(item__time__range=(0, 4)).exclude(status="prepared")
    medium = Order.objects.all().filter(item__time__range=(5, 8)).exclude(status="prepared")
    low = Order.objects.all().filter(item__time__range=(9, 13)).exclude(status="prepared")
    context = {
        'high': high,
        'medium': medium,
        'low': low,
    }
    return render(request, 'main/allorder.html', context)


@permission_required('is_superuser', raise_exception=True)
def onallorders(request):
    high = OnOrder.objects.all().filter(item__time__range=(0, 4)).exclude(status="prepared")
    medium = OnOrder.objects.all().filter(item__time__range=(5, 8)).exclude(status="prepared")
    low = OnOrder.objects.all().filter(item__time__range=(9, 13)).exclude(status="prepared")
    context = {
        'high': high,
        'medium': medium,
        'low': low,
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
    detail = DetailForm(request.POST or None)

    if detail.is_valid() and formset.is_valid():
        info = detail.save(commit=False)

        for form in formset:
            order = form.save(commit=False)
            order.user = request.user
            order.address = info.address
            order.contact = info.contact
            order.save()
        return redirect('/')

    return render(request, 'main/on_orders.html', {'formset': formset, 'detail': detail})


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


@user_passes_test(lambda u: u.is_staff, login_url='login')
def delete(request, pk):
    order = Order.objects.all().filter(table_id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/order')

    return render(request, 'main/delete.html', {'order': order})

@login_required(login_url='login')
def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        ordered=False,
    )
    messages.info(request, "Added to Cart!!Continue Shopping!!")
    return redirect("main:cart")


@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    total = bill.get("item__price__sum")
    context = {
        'cart_items':cart_items,
        'total': total,
    }
    return render(request, 'main/cart.html', context)


class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False


@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    ordered_date=timezone.now()
    cart_items.update(ordered=True,ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("main:order_details")


@login_required
def order_details(request):
    items = CartItems.objects.filter(user=request.user, ordered=True,status="Active").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    context = {
        'items':items,
        'cart_items':cart_items,
        'total': total,
        'count': count,
    }
    return render(request, 'main/order_details.html', context)


class Process:
    def __init__(self, name, arrive_time, serve_time):
        self.name = name
        self.arrive_time = arrive_time
        self.serve_time = serve_time
        self.left_serve_time = serve_time
        self.finish_time = 0
        self.cycling_time = 0
        self.w_cycling_time = 0


def schedule_queue(request):
    process_list0, process_list1, process_list2 = [], [], []
    for each in process_list:
        if each.serve_time <= 4:
            process_list0.append(each)
        elif each.serve_time <= 8:
            process_list1.append(each)
        else:
            process_list2.append(each)

    queue_list = []
    queue0 = Queue(0, process_list0)
    queue1 = Queue(1, process_list1)
    queue2 = Queue(2, process_list2)
    queue_list.append(queue0)
    queue_list.append(queue1)
    queue_list.append(queue2)

    mfq = Mulitlevelfeedbackqueue(queue_list, 2)
    mfq.scheduling()

    context = {
        "result_list": result_list
    }
    process_list.clear()
    return render(request, 'main/result_page.html', context)


class Queue:
    def __init__(self, level, process_list):
        self.level = level
        self.process_list = process_list
        self.q = 0

    def size(self):
        return len(self.process_list)

    def get(self, index):
        return self.process_list[index]

    def add(self, process):
        self.process_list.append(process)

    def delete(self, index):
        self.process_list.remove(self.process_list[index])


class RR:
    def __init__(self, process_list, q):
        self.process_list = process_list
        self.q = q

    def scheduling(self):
        process_list.sort(key=lambda x: x.arrive_time)  # according to .arrive_time Sort
        len_queue = len(self.process_list)  # The length of the process queue
        index = int(0)  # Indexes
        q = self.q  # Time slice
        running_time = int(0)  # Time already running

        # The scheduling loop
        while (True):
            if len_queue != 0:
                # The current process
                current_process = self.process_list[index % len_queue]
                # print(current_process)
                # Determine whether the current process has been completed
                if current_process.left_serve_time > 0:
                    # Calculate the completion time
                    # The service time is greater than or equal to the time slice , Then the completion time is + Time slice time The process is not over yet
                    # The service time is less than the time slice , Then the completion time is added to the original time of service
                    if current_process.left_serve_time >= q:
                        running_time += q
                        print(current_process.name, running_time, index)
                        current_process.left_serve_time -= q
                    else:
                        print('%s The service time is less than the current time slice ' % current_process.name)
                        running_time += current_process.left_serve_time
                        current_process.left_serve_time = 0
                        # Completed

                if current_process.left_serve_time == 0:
                    # Calculate the completion time
                    current_process.finish_time = running_time
                    # Calculate turnaround time
                    current_process.cycling_time = current_process.finish_time - current_process.arrive_time
                    # Calculate the turnaround time with rights
                    current_process.w_cycling_time = float(current_process.cycling_time) / current_process.serve_time
                    # Print
                    print('%s A completed process , The details are as follows ：' % current_process.name)
                    print(
                        ' Process name ：%s , Completion time ： %d , Turnaround time ：%d , Turnaround time with rights ： %.2f' % (
                            current_process.name, current_process.finish_time, current_process.cycling_time,
                            current_process.w_cycling_time))
                    result_list.append(current_process)

                    # eject
                    self.process_list.remove(current_process)
                    len_queue = len(self.process_list)
                    # After a process has completed its task ,index Go back first , Then add , To keep pointing to the next process that needs to be scheduled
                    index -= 1

            # index Regular increase
            index += 1

            # If there is no process in the queue, execution is complete
            if len(self.process_list) == 0:
                break

            # change index, Avoid it because index Greater than len, This leads to an error in taking the mold
            if index >= len(self.process_list):
                index = index % len_queue


class Mulitlevelfeedbackqueue():
    def __init__(self, queue_list, q_first):
        self.queue_list = queue_list
        self.q_first = q_first

    def scheduling(self):
        q_list = self.queue_list  # Current queue set
        q_first = self.q_first  # The time slice of the first queue

        for i in range(len(q_list)):
            # Determine the time slice for each queue
            if i == 0:
                q_list[i].q = q_first
            else:
                q_list[i].q = q_list[i - 1].q * 2

            # Time slice execution starts from the first queue
            # First judge whether it is the last queue , The last queue is executed directly RR Scheduling algorithm
            # If it's not the last queue , After executing the current queue time slice, judge whether it is necessary to join the end of the next queue
            if i == len(q_list) - 1:
                print('************** Execute on the last queue RR Scheduling algorithm *************')

                # print(q_list[i].process_list[])
                # The last queue resets the arrival time
                for t in range(len(q_list[i].process_list)):
                    q_list[i].process_list[t].arrive_time = t
                rr_last_queue = RR(q_list[i].process_list, q_list[i].q)
                rr_last_queue.scheduling()
            else:
                currentQueue = q_list[i]

                index = int(0)
                while (True):
                    if index == currentQueue.size():
                        break

                    if currentQueue.get(index).left_serve_time > q_list[i].q:
                        currentQueue.get(index).left_serve_time -= q_list[i].q
                        print(' The first %d Queue time slice : %d' % (i, q_list[i].q))
                        print(
                            ' The process is not finished , Need to be added to the end of the next queue ： Process name ：%s ' % (
                                currentQueue.get(index).name))
                        # Throw the current process to the end of the next queue
                        q_list[i + 1].add(currentQueue.get(index))
                        index += 1
                    else:
                        print(' The service completes and pops up :', currentQueue.get(index).name)
                        currentQueue.get(index).left_serve_time = 0
                        result_list.append(currentQueue.get(index))
                        currentQueue.delete(index)

                    if index == currentQueue.size():
                        break
