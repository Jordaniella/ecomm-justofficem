from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
import datetime

from store.models import Product, Order, OrderItem
from store.utils import cookie_cart, get_cart_data,guest_order, get_filter,search_products,search_products_with_filter,filter_products


def home(request):
    context = get_cart_data(request)
    return render(request, "store/pages/home.html", context)

def store(request):
    context = get_cart_data(request)
    if(request.method == "POST" ):
        form = request.POST
        print(form)
        filter_value = form["filter"]
        search_value = form["searchProd"]
        if filter_value != "" and search_value != "":
            products, context["search"] = search_products_with_filter(search_value, filter_value)
        elif filter_value != "" and search_value == "":
            products = filter_products(filter_value)
        else:
            products = Product.objects.all().order_by("id")
        context["filters"] = get_filter(filter_value)
    else:
        products = Product.objects.all().order_by("id")
        context["filters"] = get_filter("none")
    
    if (len(products) <= 0):
        context["products"] = products
    else:  
        if (len(products) >= 6):
            paginator = Paginator(products, 6)
        else: 
            paginator = Paginator(products, len(products))
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["products"] = page_obj
    
    return render(request, "store/pages/store.html", context)

def cart(request):
    context = get_cart_data(request)
    return render(request, "store/pages/cart.html", context)

def checkout(request):
    context = get_cart_data(request)
    return render(request, "store/pages/checkout.html", context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    elif action == "remove-all":
        orderItem.quantity = 0
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
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id
        
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
    else:
        customer, order = guest_order(request, data)
    
    total = float(data["form"]["total"])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    return JsonResponse("Payment submitted..", safe=False)

def see_product(request, id): 
    product = Product.objects.get(id=id)
    context = get_cart_data(request)
    context["product"] = product
    return render(request, "store/pages/product-item.html", context)

    