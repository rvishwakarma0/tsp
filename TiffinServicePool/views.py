from django.shortcuts import render,redirect
from django.http import JsonResponse 
import json
import datetime
from .models import * 
from .utils import CookieCart,cartData, guestOrder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .emails import *

def index(request):
    
    data = cartData(request)
    items = data['items']
   
    cart_items = data['cart_items']

    tiffins = Tiffin.objects.all()

    context = {'tiffins': tiffins, 'cart_items':cart_items}
    return render(request, "TiffinServicePool/index.html", context)
    



def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'items':items, 'order': order, 'cart_items':cart_items}
    return render(request, "TiffinServicePool/cart.html", context)




def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']
    context = {'items':items, 'order': order, 'cart_items':cart_items}
    return render(request, "TiffinServicePool/checkout.html", context)


def UpdateItem(request):
    data = json.loads(request.body)
    tiffinId = data['tiffinId']
    action = data['action']
    print('Action:',action)
    print('tiffinId:',tiffinId)

    customer = request.user.customer
    tiffin = Tiffin.objects.get(id=tiffinId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created= OrderItem.objects.get_or_create(order=order, tiffin=tiffin)

    if action  == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)


def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer,order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.setTransactionId()

    if total == order.get_cart_total:
        order.complete = True

    sa = ShippingAddress.objects.create(
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'])
    order.address = sa
    order.save()
    customer_order_complete_mail(customer, order)
    print(sa.address)
    print(sa.city)
    vendor_order_mail(order)
    return JsonResponse('Payment Completed', safe=False)

@login_required
def userLogout(request):
    logout(request)
    return redirect('/')


def loginOrRegister(request):
    data = cartData(request)
    cart_items = data['cart_items']

    if request.method == 'POST':
        
        formType = request.POST.get('formType')
        if formType == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user:
                login(request,user)
                return redirect('/')
            else:
                return render(request, 'TiffinServicePool/login.html', {'error_msg': 'Invalid login details given.', 'cart_items':cart_items})
        elif formType == 'register':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            defaultShippingAddress = request.POST.get('defaultShippingAddress')
            defaultShippingCity = request.POST.get('defaultShippingCity')
            defaultShippingState = request.POST.get('defaultShippingState')
            defaultShippingZipCode = request.POST.get('defaultShippingZipCode')

            try:
                user = User.objects.get(username=email)
                return render(request, 'TiffinServicePool/login.html', {'error_msg_reg': 'User already exist, proceed with login or use diffrent email id', 'cart_items':cart_items})
            except:
                user = User.objects.create(username=email)
                user.email=email
                user.set_password(password)
                user.save()
                customer, created= Customer.objects.get_or_create(email=email)

                customer.user = user
                customer.name = name

                customer.save()
                daddress, created = ShippingAddress.objects.get_or_create(customer=customer,
                                                                          address=defaultShippingAddress,
                                                                          city=defaultShippingCity,
                                                                          state=defaultShippingState,
                                                                          zipcode=defaultShippingZipCode)
                customer.defaultAddress = daddress
                customer.save()
                #welcome_mail(customer.name, customer.email) #sending welcome mail
                return render(request, 'TiffinServicePool/login.html', {'error_msg_reg': 'Successfully registered, Login Now!', 'cart_items':cart_items})


    return render(request, 'TiffinServicePool/login.html', {'cart_items':cart_items})


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
    return render(request, 'TiffinServicePool/vendor.html', context)


def myOrders(request):
    total_amt_spent = 0
    no_of_orders = 0
    data = cartData(request)
    cart_items = data['cart_items']
    if request.user.is_authenticated:
        cs = request.user.customer
        orders = cs.order_set.all()
        orders = orders[:len(orders)-1]
        for order in orders:
            total_amt_spent += order.get_cart_total
            no_of_orders += 1
    else:
        orders = []
    context = {'orders': orders,
               'cart_items':cart_items,
               'total_amt_spent': total_amt_spent,
               'no_of_orders': no_of_orders,
    }
    return render(request, "TiffinServicePool/myorders.html", context)


def my_order_details(request, id):
    items = []
    order = []
    data = cartData(request)
    cart_items = data['cart_items']
    if request.user.is_authenticated:
        cs = request.user.customer
        order = cs.order_set.get(id = id)
        items = order.orderitem_set.all()
    context = {'items':items, 'order': order, 'cart_items':cart_items}
    return render(request, "TiffinServicePool/myOrderDetails.html", context)

@login_required
def cancel_order(request, oid):
    data = cartData(request)
    cart_items = data['cart_items']
    order = Order.objects.get(id=oid)
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'True':
            order.canceled = True
            order.save()
            vendor = order.orderitems_set.all()[0]
            vendor = vendor.tiffin.vendor
            order_cancellation_mail(vendor, order)
        myOrdersUrl = '/my_orders/'+str(oid)+'/'
        return redirect(myOrdersUrl)
    context = {'order': order, 'cart_items': cart_items}
    return render(request, "TiffinServicePool/cancelOrder.html", context)


def my_account(request):
    cs = []
    data = cartData(request)
    cart_items = data['cart_items']
    if request.user.is_authenticated:
        cs = request.user.customer
    context = {
        'customer':cs,
        'cart_items': cart_items
    }
    return render(request, 'accounts/my_account.html', context)


@login_required
def rating(request,vot, id):
    data = cartData(request)
    cart_items = data['cart_items']
    vendor=[]
    tiffin=[]
    if vot == 'v':
        vendor = Vendor.objects.get(id=id)
    else:
        tiffin = Tiffin.objects.get(id=id)
    if request.method == 'POST':
        customer = request.user.customer
        rate = request.POST.get('rate')
        if vot == 'v':
            rbcov, created = RatingByCoustomerOnVendor.objects.get_or_create(customer=customer, vendor=vendor)
            rbcov.rating = rate
            rbcov.save()
            return redirect('/vendor/'+str(vendor.id)+'/')
        else:
            rbcot, created = RatingByCoustomerOnTiffin.objects.get_or_create(customer=customer, tiffin=tiffin)
            rbcot.rating = rate
            rbcot.save()
        return redirect('/my_orders/')
    context = {'tiffin': tiffin, 'vendor': vendor, 'cart_items': cart_items}
    return render(request, "TiffinServicePool/rating.html", context)


