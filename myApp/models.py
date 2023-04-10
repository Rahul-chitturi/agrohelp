from django.db import models as mo
from django.contrib.auth.models import auth, User
import datetime

Product_Category = (
    ("Equipments", "Equipments"),
    ("Fertilizers", "Fertilizers")
)


class customer(mo.Model):
    customerID = mo.BigAutoField(primary_key=True)
    user = mo.ForeignKey(to=User, on_delete=mo.CASCADE)
    address = mo.TextField(max_length=100, default='')
    pincode = mo.CharField(max_length=6, default='')
    profileImage = mo.ImageField(upload_to="Profiles")

    def __str__(self):
        return str(self.customerID)


class agricultureBasics(mo.Model):
    agriID = mo.BigAutoField(primary_key=True)
    title = mo.TextField(max_length=20, default='')
    description = mo.TextField(max_length=1000, default='')
    publishedDateTime = mo.DateTimeField(default=datetime.datetime.now())
    documents = mo.FileField(upload_to="AgroBasics")

    def __str__(self):
        return str(self.agriID)


class agricultureSchemes(mo.Model):
    schemeID = mo.BigAutoField(primary_key=True)
    title = mo.TextField(max_length=20, default='')
    description = mo.TextField(max_length=250, default='')
    startDate = mo.DateTimeField(default=datetime.datetime.now())
    lastDate = mo.DateTimeField(default=datetime.datetime.now())
    applyLink = mo.URLField(default='')

    def __str__(self):
        return str(self.schemeID)


class applications(mo.Model):
    applicationID = mo.BigAutoField(primary_key=True)
    appliedTo = mo.ForeignKey(to=agricultureSchemes, on_delete=mo.CASCADE)
    appliedBy = mo.ForeignKey(to=customer, on_delete=mo.CASCADE)
    appliedDate = mo.DateTimeField(default=datetime.datetime.now())
    applicationStatus = mo.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.applicationID)


class subscribers(mo.Model):
    subscriberID = mo.BigAutoField(primary_key=True)
    subscriberEmail = mo.EmailField(default=None)

    def __str__(self):
        return str(self.subscriberID)


class products(mo.Model):
    productID = mo.BigAutoField(primary_key=True)
    name = mo.TextField(max_length=25, default='')
    description = mo.TextField(max_length=100, default='')
    category = mo.CharField(max_length=20, choices=Product_Category, default='"Equipments')
    price = mo.IntegerField(default=0)
    quantity = mo.IntegerField(default=0)
    productImg = mo.ImageField(upload_to='Products')

    def __str__(self):
        return str(self.productID)


class cart(mo.Model):
    cartID = mo.AutoField(primary_key=True)
    customerName = mo.ForeignKey(to=customer, on_delete=mo.CASCADE)
    productName = mo.ForeignKey(to=products, on_delete=mo.CASCADE)
    quantity = mo.IntegerField(default=0)

    def __str__(self):
        return str(self.cartID)


class orders(mo.Model):
    orderID = mo.CharField(max_length=10, default=None, primary_key=True)
    customerName = mo.ForeignKey(to=customer, on_delete=mo.CASCADE)
    product = mo.ForeignKey(to=products, on_delete=mo.CASCADE)
    contactNumber = mo.TextField(max_length=10, default='')
    quantity = mo.IntegerField(default=0)
    totalPrice = mo.IntegerField(default=0)
    address = mo.TextField(max_length=250, default='')
    orderDate = mo.DateField(default=datetime.date.today())
    expectedDeliveryDate = mo.DateField(default=datetime.date.today())
    status = mo.CharField(max_length=10, default='')

    def __str__(self):
        return str(self.orderID)


class feedback(mo.Model):
    fID = mo.AutoField(primary_key=True)
    user = mo.ForeignKey(to=customer, on_delete=mo.CASCADE)
    rating = mo.IntegerField(default=0)
    opinion = mo.TextField(max_length=250, default='')

    def __str__(self):
        return str(self.fID)


class grassCutters(mo.Model):
    grassCutterID = mo.BigAutoField(primary_key=True)
    userObj = mo.ForeignKey(to=User, on_delete=mo.CASCADE)
    city = mo.TextField(max_length=20, default='')
    district = mo.TextField(max_length=20, default='')
    price = mo.IntegerField(default=0)

    def __str__(self):
        return str(self.grassCutterID)
