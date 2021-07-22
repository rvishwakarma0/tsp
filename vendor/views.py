from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from TiffinServicePool.models import *
from TiffinServicePool.utils import CookieCart,cartData, guestOrder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from TiffinServicePool.emails import *



def vendor(request, vid):
    data = cartData(request)
    cart_items = data['cart_items']
    try:
        vendorObj = Vendor.objects.get(id=vid)
    except:
        return redirect('/')
    #products = Product.objects.filter(vendor=vendorObj)
    tiffins = vendorObj.tiffin_set.all()
    print(tiffins)
    context = {
        'cart_items': cart_items,
        'tiffins': tiffins,
        'vendor': vendorObj
    }
    return render(request, 'vendor/vendor.html', context)

def dashboard(request, vid):
    total_amt_spent = 0
    no_of_orders = 0
    data = cartData(request)
    cart_items = data['cart_items']
    orders = []
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(id=vid)
        if vendor.email == request.user.email:
            orders = []
            orderitems = OrderItem.objects.all()
            for orderitem in orderitems:
                if orderitem.tiffin.vendor == vendor and orderitem.order.transaction_id is not None:
                    orders.append(orderitem)
                    total_amt_spent += orderitem.get_total
                    no_of_orders += 1
        else:
            print("Not a vendor")
    else:
        orders = []
    context = {'orders': orders,
               'cart_items':cart_items,
               'total_amt_spent': total_amt_spent,
               'no_of_orders': no_of_orders,
                'vid':vid
    }
    return render(request, "vendor/dashboard.html", context)

@login_required
def deliver(request, oid, vid):
    data = cartData(request)
    cart_items = data['cart_items']
    order = Order.objects.get(id=oid)
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'True':
            order.delivery = True
            order.save()
            vendor=Vendor.objects.get(id=vid)
            order_delivered_mail(vendor, order)
        return redirect(f'/vendor/dashboard/{vid}/')
    context = {'order': order, 'cart_items': cart_items, 'vid':vid}
    return render(request, "vendor/deliverOrder.html", context)

@login_required
def cancel_order(request, oid, vid):
    data = cartData(request)
    cart_items = data['cart_items']
    order = Order.objects.get(id=oid)
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'True':
            order.canceled = True
            order.save()
            vendor = Vendor.objects.get(id=vid)
            order_cancellation_mail(vendor, order)
        return redirect(f'/vendor/dashboard/{vid}/')
    context = {'order': order, 'cart_items': cart_items, 'vid':vid}
    return render(request, "vendor/cancelOrder.html", context)