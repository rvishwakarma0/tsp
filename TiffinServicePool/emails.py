from django.conf import settings
from django.core.mail import send_mail


def welcome_mail(name, email):
    try:
        subject = 'Welcome to Tiffin Service Pool (TSP)'
        message = f'Hi {name}, thank you for registering in TSP. Beat the Hunger with us! \n\n Regards,TSP'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        print("welcome mail sent")
    except:
        print("failed sending welcome message")
    return 1


def vendor_order_mail(order):
    try:
        recipient_list = []
        items = order.orderitem_set.all()
        for item in items:
            recipient_list.append(item.tiffin.vendor.email)
        recipient_list = list(set(recipient_list))
        subject = 'Tiffin Service Pool (TSP) Order received'
        msg = f"Hi,\n Order received with transaction id {order.transaction_id}, Please login and deliver the orders.\n\n Regards,TSP"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, msg, email_from, recipient_list)
        print("vendor order mail sent")
    except:
        print("failed sending order message to vendor")
    return 1


def customer_order_complete_mail(customer, order):
    try:
        msg = f"Hi {customer.name},\n {order.get_cart_items} tiffins of worth Rs.{order.get_cart_total} with transaction id {order.transaction_id} are successfully Ordered.\n\n Regards,TSP"
        subject = 'Tiffin Service Pool (TSP) Order Completed'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [customer.email, ]
        send_mail(subject, msg, email_from, recipient_list)
        print("customer order mail sent")
    except:
        print("failed sending order complete message to customer")
    return 1


def order_cancellation_mail(vendor, order):
    try:
        subject = 'Order cancelled (TSP)'
        message = f'Hi, Order {order.id} cancelled! \n\n Regards,TSP'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order.customer.email, vendor.email ]
        send_mail(subject, message, email_from, recipient_list)
        print("order cancelleation sent")
    except:
        print("failed sending cancel message")
    return 1

def order_delivered_mail(vendor, order):
    try:
        subject = 'Order delivered (TSP)'
        message = f'Hi, Order {order.id} delivered by the vendor. \n\n Regards,TSP'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order.customer.email, vendor.email ]
        send_mail(subject, message, email_from, recipient_list)
        print("order delivered sent!!")
    except:
        print("failed sending deliver message")
    return 1