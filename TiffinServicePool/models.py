from django.db import models
from django.contrib.auth.models import User
import datetime
Rating = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
TiffinType = (('BREAKFAST', 'BREAKFAST'), ('LUNCH','LUNCH'), ('DINNER','DINNER'))


class ShippingAddress(models.Model):
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True,unique=True)
    defaultAddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    photo1 = models.ImageField(null= True, blank=True)
    photo2 = models.ImageField(null=True, blank=True)
    photo3 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def getPhoto1(self):
        try:
            url = self.photo1.url
        except:
            url = ''
        return url

    @property
    def getPhoto2(self):
        try:
            url = self.photo2.url
        except:
            url = ''
        return url

    @property
    def getPhoto3(self):
        try:
            url = self.photo3.url
        except:
            url = ''
        return url

    @property
    def rating(self):
        customerRatings = self.ratingbycoustomeronvendor_set.all()
        totalRatings = 0
        for cr in customerRatings:
            totalRatings += cr.rating
        try:
            AvgRating = totalRatings // len(customerRatings)

        except:
            AvgRating = 0
        if (AvgRating > 5):
            AvgRating = 5
        return AvgRating


class Tiffin(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    #digital = models.BooleanField(default=True, null=True, blank=False)
    photo1 = models.ImageField(null=True, blank=True)
    photo2 = models.ImageField(null=True, blank=True)
    photo3 = models.ImageField(null=True, blank=True)
    tiffinType = models.CharField(
        max_length=10,
        choices=TiffinType,
        default='3'
    )
    description = models.CharField(max_length=500, null=True, blank=True)
    veg = models.BooleanField(default=True, null=True, blank=False)
    available = models.BooleanField(default=True, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    def getPhoto1(self):
        try:
            url = self.photo1.url
        except:
            url = ''
        return url

    @property
    def getPhoto2(self):
        try:
            url = self.photo2.url
        except:
            url = ''
        return url

    @property
    def getPhoto3(self):
        try:
            url = self.photo3.url
        except:
            url = ''
        return url

    @property
    def getDietType(self):
        if self.veg:
            return "VEG"
        else:
            return "NON-VEG"
    @property
    def getAvailability(self):
        if self.available:
            return "AVAILABLE"
        else:
            return "UNAVAILABLE"

    @property
    def rating(self):
        customerRatings = self.ratingbycoustomerontiffin_set.all()
        totalRatings = 0
        for cr in customerRatings:
            totalRatings += cr.rating
        try:
            AvgRating = totalRatings // len(customerRatings)

        except:
            AvgRating = 0

        if (AvgRating > 5):
            AvgRating = 5
        return AvgRating


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    delivery = models.BooleanField(default=False, null=True, blank=False)
    canceled = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(default="INIT_TRANS",max_length=200, null=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total    

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def setTransactionId(self):
        tstmp = str(datetime.datetime.now().timestamp())
        self.transaction_id = tstmp[:10]


class OrderItem(models.Model):
    tiffin = models.ForeignKey(Tiffin, on_delete=models.SET_NULL, blank=True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.tiffin.price * self.quantity
        return total


class RatingByCoustomerOnTiffin(models.Model):
    tiffin = models.ForeignKey(Tiffin, on_delete= models.SET_NULL, blank= True, null= True)
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, blank= True, null=True)
    rating = models.IntegerField(
        choices=Rating,
        default=0
    )

    def __str__(self):
        return str(self.rating)


class RatingByCoustomerOnVendor(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.IntegerField(
        choices=Rating,
        default=0
    )

    def __str__(self):
        return str(self.rating)