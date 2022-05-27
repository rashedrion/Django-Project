from cmath import log
from configparser import InterpolationMissingOptionError
from multiprocessing import context
import re
from unicodedata import category
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import is_valid_path
from .models import Category, Customer, Product, Order
from .forms import OrderForms, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from django.contrib import messages


@unauthenticated_user
def user_registration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        messages.success(
            request, "Account is created successfully "+username)
        return redirect('/')
    else:
        messages.info(request, 'Validation failed')
    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)


@unauthenticated_user
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "user name or password is incorrect")

    context = {}
    return render(request, 'login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['admin', 'customer'])
def index(request):
    categories = Category.objects.all()

    # key value pair
    context = {
        "categories": categories,
    }

    return render(request, "index.html", context=context)


@allowed_users(allowed_roles=['admin', 'manager'])
def show_category(request, pk):
    category = Category.objects.get(id=pk)

    context = {
        "category": category
    }
    return render(request, "category_details.html", context=context)


@allowed_users(allowed_roles=['admin', 'sales'])
def about(request):
    return render(request, "about.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer', 'manager'])
def order(request):
    form = OrderForms()

    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order-list')

    context = {
        "form": form
    }
    return render(request, "order.html", context=context)


@login_required(login_url='login')
def orderlist(request):
    orderlists = Order.objects.all()
    context = {
        "orders": orderlists
    }

    return render(request, "orderlist.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForms(instance=order)

    if request.method == "POST":
        form = OrderForms(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(orderlist)

    context = {
        'form': form
    }
    return render(request, "order.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def show_order(request, pk):
    order_details = Order.objects.get(id=pk)

    context = {
        'order': order_details
    }
    return render(request, "order_details.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    item = Order.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect(orderlist)

    context = {
        'item': item
    }
    return render(request, "delete.html", context=context)
