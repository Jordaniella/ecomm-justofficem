import json
from store.models import Product, Order, OrderItem

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Products.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            item = {
                "product": {
                    "id":product.id,
                    "name": product.name,
                    "price":product.price,
                    "imageURL": product.imageURL},
                "quantity": cart[i]["quantity"],
                "get_total":total
            }
            items.append(item)
        except: pass
    return {'cartItems':cartItems, 'order':order, 'items': items}

def get_cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cartItems = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']
    
    context = {"items":items, 'order':order,'cartItems': cartItems}
    return context

def guest_order(request, data):
    print("User is not authenticated")
    print('COOKIES : ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookie_data = cookie_cart(request)
    items = cookie_data['items']
    
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order