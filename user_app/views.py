
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
from .models import Address
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


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
        if passw.strip() == '':
            messages.error(request, "password cannot be empty")
            return redirect('user_app:login')


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
    print('logout')
    user_logout(request)
    return redirect('user_app:userhome')





def base_profile(request):
    return render(request,'userside/base-profile.html')

def profile_details(request):

    
    # return render(request, 'user_addresses.html', {'user_addresses': dummy_addresses})


    return render(request,'userside/profile-details.html')
        




def account_settings(request):
    return render(request,'')

def profile_address(request):
    user = request.user
    user_addresses = Address.objects.filter(account=user)
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'userside/profile-address.html', context)

                        
def profile_orders(request):
    return render(request,'userside/profile-orders.html')


def create_address(request):

    if request.method == "POST":
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        phone_number     = request.POST.get('phone_number')
        town_city        = request.POST.get('town_city')
        street_address   = request.POST.get('street_address')
        state            = request.POST.get('state')
        country_region   = request.POST.get('country_region')
        zip_code         = request.POST.get('zip_code')
        # image = request.FILES.get('image')

        user=request.user
        address = Address.objects.create(account=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town_city=town_city,street_address=street_address,state=state,country_region=country_region,zip_code=zip_code)
        make_default = request.POST.get('make_default')
        print(make_default)
        # Convert 'on' to True and set is_default accordingly
        is_default = make_default == 'on'
        address.is_default = is_default
        address.save()

        return redirect('user_app:profile-address')

    return render(request,'userside/profile-address-create.html')


def edit_address(request, id):
    user = request.user
    address = get_object_or_404(Address, id=id)
    
    if request.method == 'POST':
        # Handle form submission
        # Save the updated data
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.phone_number = request.POST.get('phone_number')
        address.street_address = request.POST.get('street_address')
        address.town_city = request.POST.get('town_city')
        address.state = request.POST.get('state')
        address.country_region = request.POST.get('country_region')
        address.zip_code = request.POST.get('zip_code')
        address.save()

        # Check if the address is being set as default
        # if 'make_default' in request.POST:
        #     user_addresses = Address.objects.filter(account=user)
        #     for addr in user_addresses:
        #         addr.is_default = False
        #         addr.save()
        #     address.is_default = True
        #     address.save()

        return redirect('user_app:profile-address')

    context = {
        'address': address
    }
    return render(request, 'userside/profile-address-edit.html', context)


def set_default_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id)
        
        # Unset default for all addresses of the user
        Address.objects.filter(account=request.user).update(is_default=False)
        
        # Set the selected address as default
        address.is_default = True
        address.save()
        
        return JsonResponse({'message': 'Address set as default.'})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

def delete_address(request):
    address_id = request.GET.get('id')
    print(address_id)
    address = get_object_or_404(Address, id = address_id)
    print(address.first_name)
    
    user_address = Address.objects.filter(first_name = address.first_name )
    if not user_address:
        return redirect('myaddress')
    
    user_address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('myaddress')