from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from store.models import Product, Order, OrderItem
from store.utils import cookie_cart, get_cart_data, guest_order


def home(request):
    context = {}
    return render(request, "store/home.html", context)

def store(request):
    products = Product.objects.all()
    context = get_cart_data(request)
    context["products"] = products
    return render(request, "store/store.html", context)

def cart(request):
    context = get_cart_data(request)
    return render(request, "store/cart.html", context)

def checkout(request):
    context = get_cart_data(request)
    return render(request, "store/checkout.html", context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data["action"]
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
    else:
        customer, order = guest_order(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    return JsonResponse("Payment submitted..", safe=False)