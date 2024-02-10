
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponse
from admin_app.models import User
from django.db.models import Q
import random 
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control
from store.models import Product


# signup page
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:admin_dashboard')
        return redirect('user_app:userhome')
    if request.method == "POST":
        user = request.POST["username"]
        email = request.POST["email"]
        passw = request.POST["password"]
        conpass = request.POST["conf_password"]
        try:
            if User.objects.get(email = email):
                messages.warning(request,"email is taken")
                return redirect('user_app:usersignup')
        except:
                pass

        if ' ' in user:
            messages.warning(request, "Username cannot contain whitespaces")
            return redirect('user_app:usersignup')

        if ' ' in passw:
            messages.warning(request, "Password cannot contain whitespaces")
            return redirect('user_app:usersignup')
        
        if not email or '@' not in email:
            messages.info(request,"Email id is not in correct format")
            return redirect('user_app:usersignup')
        if passw != conpass:
            messages.warning(request,"Password is incorrect")
            return redirect('user_app:usersignup')
        if len(passw) < 8:
            messages.info(request,"Password minimum 8 characters")
            return redirect('user_app:usersignup')
        randomotp = str(random.randint(1000, 9999))
        request.session['otp_key'] = randomotp
        request.session['email']=email
        request.session.modified = True 
        request.session.set_expiry(300)

        # password1 = make_password(password1)
        request.session['username'] = user
        request.session['password'] = passw
        # request.session['email']= email

        subject = "Verify Your One-Time Password (OTP) - Time Gallery Ecommerce Store"
        sendermail = "timegalleryt.com"
        otp = f"Hello,\n\nYour One-Time Password (OTP) for verification at Time Gallery Ecommerce Store is: {randomotp}\n\nThank you for choosing Time Gallery Ecommerce Store.\n\nBest regards,\nTime Gallery Ecommerce Store Team"

        send_mail(subject,otp,sendermail,[email],fail_silently=True)
        

        return render(request,'userside/otp.html')
    return render(request,'userside/usersignup.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)   
@never_cache
def otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:dashboard')
        return redirect('userhome')
    user = request.session.get('username')
    email = request.session.get('email')
    password = request.session.get('password')
    if request.method == 'POST':
        if str(request.session['otp_key']) == str(request.POST['otp']):
            customer = User.objects.create_user(username = user, email = email, password = password )
            customer.save()
            customer = authenticate(request, email=email, password=password)
            user_login(request,customer)
            return redirect('user_app:userhome')
        else:
            messages.error(request,"Invalid OTP")
            return redirect('user_app:otp')   
    return render(request,'user/otp.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect('user_app:userhome')
    
    if request.method == "POST":
        email = request.POST["email"]
        passw = request.POST["password"]

        if len(passw) < 8:
            messages.info(request,"invalid credentials")
            return redirect('user_app:login')
            
        if not User.objects.filter(email=email):
            messages.error(request, "Invalid Email Adress")
            return redirect('user_app:login')
        
        customer = User.objects.get(email=email)

        if customer.is_active == True:
            user_details = authenticate(email=email, password=passw)
            
            if user_details is not None and not user_details.is_superuser:
                user_login(request, user_details)
                return redirect('user_app:userhome')
            else:
                messages.warning(request, "Invalid credentials")
                return redirect('user_app:login')
        else:
            messages.warning(request, "Sorry you are BLOCKED")
            return redirect('user_app:login')
    
    response = render(request, 'userside/userlogin.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @never_cache

def userhome(request):

    products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active = True)  # Filter out products with no brand and inactive brands
    context = {
        'products':products
    }

    return render(request, 'userside/home.html', context)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache

def logout(request):
    # user = User.objects.get(user = request.user)
    # print(user)
    user_logout(request)
    return redirect('user_app:userhome')

