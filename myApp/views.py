import csv
import datetime
from datetime import datetime, date
import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import smtplib
import random
from .models import products, orders, customer, applications, agricultureSchemes, agricultureBasics, feedback, cart, \
    subscribers, grassCutters, Job
from .forms import ProductForm, AgroBasicForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import urllib.request
from IPython.display import HTML
import requests
import re


def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        obj = customer.objects.get(user=request.user)
        return render(request, 'home.html', {'customer': obj})
    return render(request, 'home.html')


def team(request):
    return render(request, 'team.html')


def contactUs(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['message']
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("4su18cs017@sdmit.in", "Bharath@B26")
            message = "Subject : Message from {} \n\nName : {}\nEmail : {}\n{}".format(name, name, email, msg)
            s.sendmail(email, "4su18cs017@sdmit.in", message)
            s.quit()
            messages.success(request, 'Successfully sent.')
            return redirect('home')
        except:
            messages.error(request, 'Unable to sent ..')
            return redirect('home')
    else:
        return render(request, 'contactUs.html')


def services(request):
    return render(request, 'services.html')


def subscribe(request):
    if request.method == "POST":
        subscriberEmail = request.POST['email']
        if subscribers.objects.filter(subscriberEmail=subscriberEmail).exists():
            messages.success(request, 'Already subscribed.')
        else:
            obj = subscribers(subscriberEmail=subscriberEmail)
            obj.save()
            messages.success(request, 'Thank you for your subscription')
        return redirect('home')


def sendInfo(subject, message):
    obj = subscribers.objects.all()
    l1 = []
    for i in obj:
        l1.append(str(i.subscriberEmail))
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("4su18cs017@sdmit.in", "Bharath@B26")
        text = "Subject : {} \n\n {}".format(subject, message)
        s.sendmail("4su18cs017@sdmit.in", l1, text)
        s.quit()
        return True
    except:
        return False


def adminLogin(request):
    if request.method == "POST":
        uname = request.POST['username']
        p = request.POST['password']
        a = auth.authenticate(username=uname, password=p)
        if a is not None:
            if a.is_superuser:
                auth.login(request, a)
                return redirect('adminMenu')
            else:
                messages.error(request, 'Username or Password is wrong.')
                return redirect('adminLogin')
        else:
            messages.error(request, 'Username or Password is wrong.')
            return redirect('adminLogin')
    else:
        return render(request, 'admin/login.html')


@login_required(login_url='/admin/login')
def adminLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home')


@login_required(login_url='/admin/login')
def adminMenu(request):
    if request.user.is_superuser:
        obj = len(list(customer.objects.all()))
        obj1 = len(list(products.objects.all()))
        obj2 = len(list(orders.objects.all()))
        obj3 = len(list(applications.objects.all()))
        obj4 = feedback.objects.all()
        return render(request, 'admin/admin-menu.html',
                      {'customers': obj, 'products': obj1, 'orders': obj2, 'applications': obj3, 'feedbacks': obj4})
    else:
        messages.error(request, 'You need to login to access this page.')
        return redirect('adminLogin')


@login_required(login_url='/admin/login')
def usersList(request):
    if request.user.is_superuser:
        obj = customer.objects.all()
        return render(request, 'admin/users-list.html', {'customers': obj})


@login_required(login_url='/admin/login')
def blockUser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            Username = request.POST['username']
            try:
                obj = User.objects.get(username=Username)
            except:
                obj = None
            if obj is not None:
                obj.delete()
                messages.success(request, 'User is removed successfully.')
                return redirect('usersList')


@login_required(login_url='/admin/login')
def adminRegister(request):
    if request.user.is_superuser and request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist.')
            return redirect('adminRegister')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('adminRegister')
        elif len(password) < 8:
            messages.error(request, 'Minimum Password length is 8 or more.')
            return redirect('adminRegister')
        else:
            obj = User.objects.create_superuser(first_name=name, email=email, username=username, password=password)
            obj.save()
            messages.success(request, 'Admin is created successfully.')
            return redirect('adminList')
    else:
        return render(request, 'admin/admin-register.html')


@login_required(login_url='admin/login')
def deleteAdmin(request):
    if request.user.is_superuser:
        if request.method == "POST":
            userID = request.POST['username']
            obj = User.objects.get(username=userID)
            obj.delete()
            messages.success(request, 'Admin is removed successfully.')
            return redirect('adminList')


@login_required(login_url='/admin/login')
def adminList(request):
    if request.user.is_superuser:
        obj = User.objects.filter(is_superuser=True)
        return render(request, 'admin/admin-list.html', {'admins': obj})


@login_required(login_url='/admin/login')
def ordersList(request):
    if request.user.is_superuser:
        obj = orders.objects.all()
        return render(request, 'admin/orders-list.html', {'orders': obj})


@login_required(login_url='/admin/login')
def applicationsList(request):
    if request.user.is_superuser:
        return render(request, 'admin/application-list.html')


@login_required(login_url='/admin/login')
def agroBasicList(request):
    if request.user.is_superuser:
        obj = agricultureBasics.objects.all()
        return render(request, 'admin/agro-basic-list.html', {'agroBasics': obj})


@login_required(login_url='/admin/login')
def addBasic(request):
    if request.user.is_superuser and request.method == "POST":
        form = AgroBasicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            s = "New Information is added.."
            m = "Hello guys, Now we have added a new agricultural information\nI think it will be helpful for you.."
            sendInfo(s, m)
            messages.success(request, 'Information is added successfully.')
        else:
            messages.error(request, 'Error.')
        return redirect('agroBasicList')
    elif request.user.is_superuser:
        form1 = AgroBasicForm()
        return render(request, 'admin/add-basic.html', {'form': form1})
    else:
        messages.error(request, 'You need to login to access this page.')
        return redirect('adminLogin')


@login_required(login_url="/admin/login")
def viewDocument(request):
    if request.user.is_superuser and request.method == "POST":
        agriID = request.POST['agriID']
        obj = agricultureBasics.objects.get(agriID=agriID)
        documentName = str(obj.documents)
        fs = FileSystemStorage()
        filename = documentName
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
                response[
                    'Content-Disposition'] = 'inline; filename="mypdf.pdf"'  # user will be prompted display the PDF in the browser
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')


@login_required(login_url='/admin/edit')
def deleteAgroBasic(request):
    if request.user.is_superuser and request.method == "POST":
        agriID = request.POST['agriID']
        obj = agricultureBasics.objects.get(agriID=agriID)
        obj.delete()
        messages.success(request, 'Information is deleted successfully')
        return redirect('agroBasicList')


@login_required(login_url="/admin/login")
def productsList(request):
    if request.user.is_superuser:
        obj = products.objects.all()
        return render(request, 'admin/product-list.html', {'item': obj})


@login_required(login_url='/admin/login')
def addProduct(request):
    if request.user.is_superuser and request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            s = "New Product is added.."
            m = "Hello guys, Now we have added a new agricultural product\nI think it will be helpful for you.."
            sendInfo(s, m)
            messages.success(request, 'Product is added.')
        else:
            messages.error(request, 'Error')
        return redirect('productsList')
    elif request.user.is_superuser:
        form1 = ProductForm()
        return render(request, 'admin/add-product.html', {'form': form1})
    else:
        pass


@login_required(login_url='/admin/login')
def editProduct(request):
    if request.user.is_superuser:
        if request.method == "POST":
            id = request.POST['productID']
            try:
                obj = products.objects.get(productID=id)
            except:
                obj = None
            if obj is not None:
                return render(request, 'admin/edit-product.html', {'product': obj})
            else:
                messages.error(request, 'Product not found..')
                return redirect('productsList')


@login_required(login_url='/admin/login')
def editProductDetails(request):
    if request.user.is_superuser and request.method == "POST":
        productID = request.POST['productID']
        productName = request.POST['productName']
        productDescription = request.POST['productDescription']
        productCategory = request.POST['productCategory']
        productPrice = request.POST['productPrice']
        productQuantity = request.POST['productQuantity']
        try:
            obj = products.objects.get(productID=productID)

        except:
            obj = None

        if obj is not None:
            obj.name = productName
            obj.description = productDescription
            obj.category = productCategory
            obj.price = productPrice
            obj.quantity = productQuantity
            obj.save()
            messages.success(request, 'Edited Successfully.')
            return redirect('productsList')


@login_required(login_url='/admin/login')
def deleteProduct(request):
    if request.user.is_superuser:
        if request.method == "POST":
            productID = request.POST['productID']
            obj = products.objects.get(productID=productID)
            obj.delete()
            messages.success(request, 'Product is deleted.')
            return redirect('productsList')


@login_required(login_url='/admin/login')
def schemesList(request):
    if request.user.is_superuser:
        obj = agricultureSchemes.objects.all()
        return render(request, 'admin/schemes-list.html', {'schemes': obj})


@login_required(login_url='/admin/login')
def addScheme(request):
    if request.user.is_superuser:
        if request.method == "POST":
            title = request.POST['title']
            desc = request.POST['desc']
            sdate = request.POST['sdate']
            ldate = request.POST['ldate']
            link = request.POST['link']
            if agricultureSchemes.objects.filter(title=title).exists():
                messages.error(request, "Already present.")
                return redirect('schemesList')
            else:
                obj = agricultureSchemes(title=title, description=desc, startDate=sdate, lastDate=ldate, applyLink=link)
                obj.save()
                s = "New Scheme is added.."
                m = "Hello guys, Now we have added a new agricultural scheme released by the government\nI think it " \
                    "will be helpful for you.. "
                sendInfo(s, m)
                messages.success(request, 'Scheme is added.')
                return redirect('schemesList')
        else:
            return render(request, 'admin/add-scheme.html')


@login_required(login_url='/admin/login')
def editScheme(request):
    if request.user.is_superuser:
        if request.method == "POST":
            schemeID = request.POST['schemeID']
            obj = agricultureSchemes.objects.get(schemeID=schemeID)
            return render(request, 'admin/edit-scheme.html', {'scheme': obj})


@login_required(login_url='/admin/login')
def editSchemeDetails(request):
    if request.user.is_superuser:
        if request.method == "POST":
            schemeID = request.POST['schemeID']
            schemeTitle = request.POST['schemeTitle']
            schemeDescription = request.POST['schemeDescription']
            schemeStartDate = request.POST['schemeStartDate']
            schemeLastDate = request.POST['schemeLastDate']
            print(type(schemeStartDate))
            schemeApplyLink = request.POST['schemeApplyLink']
            obj = agricultureSchemes.objects.get(schemeID=schemeID)
            obj.title = schemeTitle
            obj.description = schemeDescription
            if not schemeStartDate == "":
                obj.startDate = schemeStartDate
            if not schemeLastDate == "":
                obj.lastDate = schemeLastDate
            obj.applyLink = schemeApplyLink
            obj.save()
            messages.success(request, 'Scheme is edited.')
            return redirect("schemesList")


@login_required(login_url='/admin/login')
def deleteScheme(request):
    if request.user.is_superuser:
        if request.method == "POST":
            schemeID = request.POST['schemeID']
            obj = agricultureSchemes.objects.get(schemeID=schemeID)
            obj.delete()
            messages.success(request, 'Scheme is deleted.')
            return redirect('schemesList')


@login_required(login_url='/admin/login')
def feedbacksList(request):
    if request.user.is_superuser:
        obj = feedback.objects.all()
        print(obj)
        return render(request, 'admin/feedbacks-list.html', {'feedbacks': obj})


@login_required(login_url='/admin/login')
def orderDetails(request):
    if request.user.is_superuser and request.method == "POST":
        orderID = request.POST['orderID']
        obj = orders.objects.get(orderID=orderID)
        return render(request, 'admin/order-details.html', {'order': obj})


@login_required(login_url="/admin/login")
def subscribersList(request):
    obj = subscribers.objects.all()
    return render(request, 'admin/subscribers-list.html', {'list': obj})


@login_required(login_url='/admin/login')
def deleteSubscription(request):
    if request.user.is_superuser and request.method == "POST":
        ID = request.POST['subscriberID']
        obj = subscribers.objects.get(subscriberID=ID)
        obj.delete()
        messages.success(request, 'Subscription is cancelled.')
        return redirect('subscribersList')


@login_required(login_url='/admin/login')
def adminGrassCuttersList(request):
    if request.user.is_authenticated:
        obj = grassCutters.objects.all()
        return render(request, 'admin/grass-cutters-list.html', {'cutter': obj})


@login_required(login_url='/admin/login')
def deleteGrassCutter(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            gID = request.POST['gID']
            obj = grassCutters.objects.get(grassCutterID=gID)
            obj.delete()
            messages.error(request, 'Deleted Successfully.')
            return redirect('adminGrassCutterList')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        obj = auth.authenticate(username=username, password=password)
        if obj is not None:
            auth.login(request, obj)
            messages.success(request, 'Logged In Successfully..')
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is wrong...')
            return redirect('userLogin')
    else:
        return render(request, 'user/login.html')


@login_required(login_url='/user/login')
def userLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home')


name = ''
username = ''
password = ''
email = ''


def userRegister(request):
    global name, email, username, password
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['contact']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist.')
            return redirect('userLogin')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist.')
            return redirect('userLogin')
        elif len(password) < 8:
            messages.error(request, 'Minimum Password is length is 8.')
            return redirect('userLogin')
        else:
            name = name
            username = username
            password = password
            email = email
            return redirect('completeSetup')


def completeSetup(request):
    global name, username, password, email
    if request.method == "POST":
        address = request.POST['address']
        pincode = request.POST['pincode']
        role = request.POST['roles']
        print(type)
        if len(pincode) == 6:
            obj = User.objects.create_user(first_name=name, email=email, username=username, password=password)
            obj.save()
            customerObj = customer(user=obj, address=address, pincode=pincode, role=role)
            customerObj.save()
            auth.login(request, obj)
            messages.success(request, 'User is created successfully.')
            return redirect('home')
    else:
        return render(request, 'user/completeSetup.html')


otp1 = 0
userEmail = ''


def forgotPassword(request):
    global otp1, userEmail
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            number = random.randint(1000, 9999)
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("4su18cs017@sdmit.in", "Bharath@B26")
                message = "Subject : Reset your Password \n\nOne Time Password : {}".format(number)
                s.sendmail("4su18cs017@sdmit.in", email, message)
                userEmail = email
                otp1 = number
                s.quit()
                return redirect('otp')
            except:
                messages.error(request, 'Unable to sent ..')
                return redirect('forgotPassword')
        else:
            messages.error(request, 'Email is not exists..')
            return redirect('forgotPassword')
    else:
        return render(request, 'user/forgot-password.html')


def otp(request):
    global otp1
    if request.method == 'POST':
        n1 = request.POST['n1']
        n2 = request.POST['n2']
        n3 = request.POST['n3']
        n4 = request.POST['n4']
        n = n1 + n2 + n3 + n4
        print(n)
        print(otp1)
        if str(otp1) == str(n):
            print("OK")
            return redirect('changePassword')
        else:
            print("Not OK")
            messages.error(request, 'OTP is wrong')
            return redirect('otp')
    else:
        return render(request, 'user/otp.html')


def changePassword(request):
    global userEmail
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(userEmail)
        if pass1 == pass2:
            obj = User.objects.get(email=userEmail)
            obj.set_password(pass1)
            obj.save()
            messages.success(request, 'Password is changed successfully')
            return redirect('userLogin')
        else:
            messages.error(request, 'Mismatched Password')
            return redirect('changePassword')
    else:
        return render(request, 'user/change-passowrd.html')


@login_required(login_url='/user/login')
def userProfile(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminMenu')
        else:
            obj = customer.objects.get(user=request.user)
            return render(request, 'user/profile.html', {'customer': obj})
    else:
        return redirect('userLogin')


@login_required(login_url='/user/login')
def feedbackForm(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            sender = request.user.username
            print(sender)
            rating = request.POST['rating']
            opinion = request.POST['opinion']

            obj = User.objects.get(username=sender)
            customerObj = customer.objects.get(user=obj)
            feedbackObj = feedback(user=customerObj, rating=rating, opinion=opinion)
            feedbackObj.save()
            return redirect('userProfile')
        else:
            return render(request, 'user/feedback-form.html')


def equipments(request):
    obj = products.objects.filter(category="Equipments").order_by("productID")
    paginator = Paginator(obj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/view-product.html', {'products': page_obj})


def fertilizers(request):
    obj = products.objects.filter(category="Fertilizers").order_by("productID")
    paginator = Paginator(obj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/view-product.html', {'products': page_obj})


@login_required(login_url='/user/login')
def myCart(request):
    if request.user.is_authenticated:
        obj = User.objects.get(username=request.user.username)
        customerObj = customer.objects.get(user=obj)
        cartItems = cart.objects.filter(customerName=customerObj).order_by("cartID")

        paginator = Paginator(cartItems, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        subtotal = 0
        totalItems = 0

        for i in cartItems:
            total = i.productName.price * i.quantity
            subtotal += total
            totalItems += i.quantity

        shippingCharge = totalItems * 70
        mainTotal = subtotal + shippingCharge
        return render(request, 'user/my-cart.html',
                      {'cart': page_obj, 'subtotal': subtotal, 'shippingCharge': shippingCharge,
                       'total': mainTotal})


@login_required(login_url='/user/login')
def addToCart(request):
    if request.user.is_authenticated and request.method == "POST":
        obj = User.objects.get(username=request.user.username)
        customerObj = customer.objects.get(user=obj)
        productID = request.POST['productID']
        productObj = products.objects.get(productID=productID)
        if cart.objects.filter(customerName=customerObj, productName=productObj).exists():
            obj = cart.objects.get(customerName=customerObj, productName=productObj)
            obj.quantity += 1
            obj.save()
        else:
            cartObj = cart(customerName=customerObj, productName=productObj, quantity=1)
            cartObj.save()
        messages.success(request, 'Item is added.')
        return redirect('myCart')


@login_required(login_url='/user/login')
def removeFromCart(request):
    if request.user.is_authenticated and request.method == "POST":
        cartID = request.POST['cartID']
        obj = cart.objects.get(cartID=cartID)
        obj.delete()
        messages.success(request, 'Item is removed.')
        return redirect('myCart')


@login_required(login_url='/user/login')
def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            productID = request.POST['productID']
            return render(request, 'user/check-out.html', {'productID': productID})


def schemes(request):
    obj = agricultureSchemes.objects.all()
    return render(request, 'user/schemes.html', {'schemes': obj})


def viewDetails(request):
    if request.method == "POST":
        productID = request.POST['productID']
        obj = products.objects.get(productID=productID)
        return render(request, 'user/view-details.html', {'item': obj})


def updateDate():
    today = date.today()
    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%y")
    newDate = str(int(day) + 3)
    date_time_str = '{}/{}/{}'.format(year, month, newDate)
    date_time_obj = datetime.strptime(date_time_str, '%y/%m/%d')
    updatedDate = date_time_obj.date()
    return updatedDate


@login_required(login_url='/user/login')
def placeOrder(request):
    if request.user.is_authenticated and request.method == "POST":
        productID = request.POST['productID']
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        quantity = request.POST['quantity']

        obj = products.objects.get(productID=productID)
        userObj = User.objects.get(username=request.user.username)
        customerObj = customer.objects.get(user=userObj)
        if int(quantity) <= obj.quantity:
            subtotal = int(quantity) * int(obj.price)
            shippingCharge = int(quantity) * 100
            totalPrice = shippingCharge + subtotal
            deliveryAddress = '{}\n{}\n{} {} {}'.format(name, address, city, state, pincode)
            S = 10
            orderID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

            updatedDate = updateDate()
            print(updatedDate)
            print("The randomly generated string is : " + str(orderID))
            obj1 = orders(orderID=str(orderID), customerName=customerObj, product=obj, contactNumber=str(contact),
                          quantity=int(quantity), totalPrice=totalPrice, address=deliveryAddress,
                          orderDate=date.today(),
                          expectedDeliveryDate=updatedDate, status="Ordered")
            obj1.save()
            obj.quantity -= int(quantity)
            obj.save()
            m = "Thank you for your order."
            s = "Your Order ID : {}\nYour order has been placed.".format(orderID)
            sendInfo(s, m)
            return render(request, 'user/invoice.html',
                          {'order': obj1, 'subtotal': subtotal, 'shippingCharge': shippingCharge})
        else:
            messages.error(request, 'Not available right now.')
            return redirect('home')


@login_required(login_url='/user/login')
def invoice(request):
    if request.user.is_authenticated:
        return render(request, 'user/invoice.html')


@login_required(login_url='/admin/login')
def deleteOrder(request):
    if request.user.is_superuser:
        if request.method == "POST":
            orderID = request.POST['orderID']
            obj = orders.objects.get(orderID=orderID)
            obj.delete()
            messages.success(request, 'Deleted Successfully.')
            return redirect('ordersList')


@login_required(login_url='/admin/login')
def editOrder(request):
    if request.user.is_superuser:
        if request.method == "POST":
            orderID = request.POST['orderID']
            obj = orders.objects.get(orderID=orderID)
            return render(request, 'admin/edit-order.html', {'order': obj})


@login_required(login_url='/admin/login')
def editOrderDetails(request):
    if request.user.is_superuser and request.method == "POST":
        orderID = request.POST['orderID']
        obj = orders.objects.get(orderID=orderID)
        obj.status = request.POST['status']
        obj.save()
        messages.success(request, 'Updated Successfully.')
        return redirect('ordersList')


@login_required(login_url='/user/login')
def myOrders(request):
    if request.user.is_authenticated:
        customerObj = customer.objects.get(user=request.user)
        orderItems = orders.objects.filter(customerName=customerObj).order_by("orderID")
        paginator = Paginator(orderItems, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user/my-orders.html', {'orders': page_obj})


@login_required(login_url='/user/login')
def cancelOrder(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            orderID = request.POST['orderID']
            obj = orders.objects.get(orderID=orderID)
            if obj.status == "Ordered":
                obj.status = 'Cancelled'
                obj.save()
                quantity = obj.quantity
                productID = obj.product.productID
                obj2 = products.objects.get(productID=productID)
                obj2.quantity += quantity
                obj2.save()
                messages.success(request, 'Your order is cancelled.')
                return redirect('home')
            else:
                messages.success(request, 'Sorry.You can\'t cancel your order.')
                return redirect('home')
        else:
            return redirect('myOrders')


@login_required(login_url='/user/login')
def trackOrder(request):
    if request.user.is_authenticated and request.method == "POST":
        orderID = request.POST['orderID']
        obj = orders.objects.get(orderID=orderID)
        return render(request, 'user/track-order.html', {'order': obj})


arecanut = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=140&VarCode=1&Date=12/10/2018&CommName=Arecanut%20/%20%E0%B2%85%E0%B2%A1%E0%B2%BF%E0%B2%95%E0%B3%86&VarName=Red%20/%20%E0%B2%95%E0%B3%86%E0%B2%82%E0%B2%AA%E0%B3%81"
wheat = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=1&VarCode=25&Date=17/05/2022&CommName=Wheat%20/%20%E0%B2%97%E0%B3%8B%E0%B2%A7%E0%B2%BF&VarName=Mexican%20/%20%E0%B2%AE%E0%B3%86%E0%B2%95%E0%B3%8D%E0%B2%B8%E0%B2%BF%E0%B2%95%E0%B2%A8%E0%B3%8D"
paddy = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=2&VarCode=1&Date=17/05/2022&CommName=Paddy%20/%20%E0%B2%AD%E0%B2%A4%E0%B3%8D%E0%B2%A4&VarName=Paddy%20/%20%E0%B2%AD%E0%B2%A4%E0%B3%8D%E0%B2%A4-1"
jowar = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=5&VarCode=2&Date=17/05/2022&CommName=Jowar%20/%20%E0%B2%9C%E0%B3%8B%E0%B2%B3&VarName=Jowar%20(%20White)%20/%20%E0%B2%9C%E0%B3%8B%E0%B2%B3%20%E0%B2%AC%E0%B2%BF%E0%B2%B3%E0%B2%BF"
onion = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=23&VarCode=9&Date=17/05/2022&CommName=Onion%20/%20%E0%B2%88%E0%B2%B0%E0%B3%81%E0%B2%B3%E0%B3%8D%E0%B2%B3%E0%B2%BF&VarName=Bellary%20Red%20/%20%E0%B2%AC%E0%B2%B3%E0%B3%8D%E0%B2%B3%E0%B2%BE%E0%B2%B0%E0%B2%BF%20%E0%B2%B8%E0%B2%A3%E0%B3%8D%E0%B2%A3"
tomato = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=78&VarCode=4&Date=17/05/2022&CommName=Tomato%20/%20%E0%B2%9F%E0%B3%8A%E0%B2%AE%E0%B3%8D%E0%B2%AF%E0%B2%BE%E0%B2%9F%E0%B3%8A&VarName=Hybrid%20/%20%E0%B2%B9%E0%B3%88%E0%B2%AC%E0%B3%8D%E0%B2%B0%E0%B2%BF%E0%B2%A1%E0%B3%8D"
potato = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=24&VarCode=14&Date=17/05/2022&CommName=Potato%20/%20%E0%B2%86%E0%B2%B2%E0%B3%82%E0%B2%97%E0%B2%A1%E0%B3%8D%E0%B2%A1%E0%B3%86&VarName=Local%20/%20%E0%B2%B8%E0%B3%8D%E0%B2%A5%E0%B2%B3%E0%B3%80%E0%B2%AF"
lemon = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=180&VarCode=1&Date=17/05/2022&CommName=Lime%20(Lemon)%20/%20%E0%B2%A8%E0%B2%BF%E0%B2%82%E0%B2%AC%E0%B3%86%E0%B2%B9%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%81&VarName=Lime%20(Lemon)%20/%20%E0%B2%A8%E0%B2%BF%E0%B2%82%E0%B2%AC%E0%B3%86%E0%B2%B9%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%81"
apple = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=17&VarCode=23&Date=17/05/2022&CommName=Apple%20/%20%E0%B2%B8%E0%B3%87%E0%B2%AC%E0%B3%81&VarName=Apple%20/%20%E0%B2%B8%E0%B3%87%E0%B2%AC%E0%B3%81"
orange = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Var&CommCode=18&VarCode=6&Date=17/05/2022&CommName=Orange%20/%20%E0%B2%95%E0%B2%BF%E0%B2%A4%E0%B3%8D%E0%B2%A4%E0%B2%B3%E0%B3%86&VarName=Orange%20/%20%E0%B2%95%E0%B2%BF%E0%B2%A4%E0%B3%8D%E0%B2%A4%E0%B2%B3%E0%B3%86"
mango = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=20&VarCode=3&Date=17/05/2022&CommName=Mango%20/%20%E0%B2%AE%E0%B2%BE%E0%B2%B5%E0%B2%BF%E0%B2%A8%E0%B2%B9%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%81&VarName=Totapuri%20/%20%E0%B2%A4%E0%B3%8B%E0%B2%A4%E0%B2%BE%E0%B2%AA%E0%B3%81%E0%B2%B0%E0%B2%BF"
banana = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx?Rep=Com&CommCode=19&VarCode=5&Date=17/05/2022&CommName=Banana%20/%20%E0%B2%AC%E0%B2%BE%E0%B2%B3%E0%B3%86%E0%B2%B9%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%81&VarName=Medium%20/%20%E0%B2%AE%E0%B2%A7%E0%B3%8D%E0%B2%AF%E0%B2%AE"


def getData(item):
    req = urllib.request.urlopen(item).read()
    soup = BeautifulSoup(req, "html.parser")
    file = open('C:/Users/Bharath/projects/agrohelp/templates/user/crop-price.html', "w")
    for link in soup.find_all('table', attrs={'id': re.compile("_ctl0_content5_Table1")}):
        soup_link = str(link)
        link = " <title>Agro-Help</title>" \
               "{% load static %}" \
               " <link rel=\"stylesheet\"  href=\"{% static 'user/crop-price.css' %}\">"
        file.write(link)
        file.write(soup_link)
    file.flush()
    file.close()


@login_required(login_url='/user/login')
def selectCrop(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            cropName = request.POST['cropName']
            if cropName == "Arecanut":
                getData(arecanut)
            elif cropName == "Wheat":
                getData(wheat)
            elif cropName == "Paddy":
                getData(paddy)
            elif cropName == "Jowar":
                getData(jowar)
            elif cropName == "Onion":
                getData(onion)
            elif cropName == "Potato":
                getData(potato)
            elif cropName == "Tomato":
                getData(tomato)
            elif cropName == "Lemon":
                getData(lemon)
            elif cropName == "Mango":
                getData(mango)
            elif cropName == "Apple":
                getData(apple)
            elif cropName == "Orange":
                getData(orange)
            else:
                getData(banana)
            return render(request, 'user/crop-price.html')
        else:
            return render(request, 'user/select-crop.html')


def agroBasics(request):
    obj = agricultureBasics.objects.all()
    return render(request, 'user/agro-basic.html', {'items': obj})


def viewBasic(request):
    if request.method == "POST":
        agriID = request.POST['agriID']
        obj = agricultureBasics.objects.get(agriID=agriID)
        return render(request, 'user/view-basic.html', {'data': obj})


@login_required(login_url="/user/login")
def viewBasicDocument(request):
    agriID = request.POST['agriID']
    obj = agricultureBasics.objects.get(agriID=agriID)
    documentName = str(obj.documents)
    fs = FileSystemStorage()
    filename = documentName
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
            response[
                'Content-Disposition'] = 'inline; filename="mypdf.pdf"'  # user will be prompted display the PDF in the browser
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')


otpVerify = 0
updatedEmail = ''


def otpVerification(request):
    global otpVerify
    if request.method == 'POST':
        n1 = request.POST['n1']
        n2 = request.POST['n2']
        n3 = request.POST['n3']
        n4 = request.POST['n4']
        n = n1 + n2 + n3 + n4
        print(n)
        print(otp1)
        if str(otpVerify) == str(n):
            print("OK")
            return redirect('confirmUpdateEmail')
        else:
            print("Not OK")
            messages.error(request, 'OTP is wrong')
            return redirect('otpVerification')
    else:
        return render(request, 'user/otpVerification.html')


@login_required(login_url='/user/login')
def emailUpdate(request):
    global otpVerify, updatedEmail
    if request.user.is_authenticated:
        if request.method == "POST":
            newEmail = request.POST['new_email']
            confirm_email = request.POST['confirm_email']
            if newEmail == confirm_email:
                number = random.randint(1000, 10000)
                try:
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    subject = "Verify your account"
                    message = "Your One Time Password is : {}".format(number)
                    s.login("4su18cs017@sdmit.in", "Bharath@B26")
                    text = "Subject : {} \n\n {}".format(subject, message)
                    s.sendmail("4su18cs017@sdmit.in", newEmail, text)
                    s.quit()
                    print("Sent")
                    otpVerify = number
                    updatedEmail = newEmail
                    return redirect('otpVerification')
                except:
                    print("Not Sent")
                    return redirect('emailUpdate')
            else:
                print("Not same")
                return redirect('emailUpdate')
        else:
            return render(request, 'user/Email-Update.html')


@login_required(login_url='/user/login')
def confirmUpdateEmail(request):
    global updatedEmail
    obj = User.objects.get(username=request.user.username)
    obj.email = updatedEmail
    obj.save()
    return redirect('userProfile')


@login_required(login_url='/user/login')
def changeNumber(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            number1 = request.POST['number1']
            number2 = request.POST['number2']
            if number1 == number2:
                if User.objects.filter(username=number1).exists():
                    print("Already Exists")
                    return redirect('changeNumber')
                else:
                    obj = User.objects.get(username=request.user.username)
                    obj.username = number1
                    obj.save()
                    return redirect('userProfile')
        else:
            return render(request, 'user/MobileNumber-Update.html')


@login_required(login_url='user/login')
def grassCutterRegistration(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            district = request.POST['district']
            city = request.POST['city']
            price = request.POST['price']
            userObj = User.objects.get(username=request.user.username)
            if grassCutters.objects.filter(userObj=userObj).exists():
                print("Already exists")
                return redirect('home')
            else:
                obj = grassCutters(userObj=userObj, city=city, district=district, price=price)
                obj.save()
                return redirect('home')
        else:
            return render(request, 'user/Cutter-Registration.html')


@login_required(login_url='user/login')
def postJob(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            pincode = request.POST['pincode']
            salary = request.POST['salary']
            workforce = request.POST['workforce']
            jobType = request.POST['type']
            hours = request.POST['hours']
            userObj = User.objects.get(username=request.user.username)

            obj = Job(userObj=userObj, pincode=pincode,
                      salary=salary, workforce=workforce, jobType=jobType)
            obj.save()
            return redirect('home')
        else:
            return render(request, 'user/PostJob.html')

@login_required(login_url='user/login')
def listJobs(request):
    if request.user.is_authenticated:
        userObj = User.objects.get(username=request.user.username)
        address = customer.objects.filter(user=userObj)
        pincode = 584123
        for i in list(address):
            pincode = i.pincode
        related_jobs = Job.objects.filter(pincode=pincode)
        return render(request, 'user/ListJobs.html',{'jobs': related_jobs})


def grassCuttersList(request):
    if request.method == "POST":
        city = request.POST['city']
        district = request.POST['district']
        obj = grassCutters.objects.filter(city=city, district=district)
        paginator = Paginator(obj, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user/Grass-Cutters-List.html', {'cutters': page_obj})
    else:
        return render(request, 'user/Location.html')
