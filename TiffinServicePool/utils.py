import json
from . models import *
from django.contrib.auth.models import User


def CookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('Cart:',cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cart_items = order['get_cart_items']

        for i in cart:
            try:
                cart_items += cart[i]["quantity"]
                tiffin = Tiffin.objects.get(id=i)
                total = (tiffin.price * cart[i]["quantity"])
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]["quantity"]

                item = {
                    'tiffin':{
                        'id': tiffin.id,
                        'name': tiffin.name,
                        'price': tiffin.price,
                        'getPhoto1': tiffin.getPhoto1
                    },
                    'quantity' : cart[i]['quantity'],
                    'get_total' : total,
                }
                items.append(item)
            except:
                pass
        return {'items':items, 'order':order, 'cart_items':cart_items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        CookieData = CookieCart(request)
        items = CookieData['items']
        order = CookieData['order']
        cart_items = CookieData['cart_items']

    return {'items':items, 'order':order, 'cart_items':cart_items}



def guestOrder(request, data):
    print("user is not logged in. . .")
    print('cookies:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = CookieCart(request)
    items = cookieData['items']
    user, created = User.objects.get_or_create(username= email)
    user.email = email
    user.save()
    customer, created = Customer.objects.get_or_create(user=user)
    customer.email = email
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False
    )
    for item in items:
        tiffin = Tiffin.objects.get(id=item['tiffin']['id'])
        ordItem = OrderItem.objects.create(
            tiffin=tiffin,
            order = order,
            quantity = item['quantity']
        )
        ordItem.save()
    return customer, order