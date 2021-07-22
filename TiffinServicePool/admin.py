from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Tiffin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Vendor)
admin.site.register(RatingByCoustomerOnTiffin)
admin.site.register(RatingByCoustomerOnVendor)
