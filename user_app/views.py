
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponse
# from TimeGallery.admin_app import models
from admin_app.models import User,UserImage
from django.db.models import Q
import random 
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control
from store.models import Product,Product_Variant
from .models import Address
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import models
from cart_app.views import _cart_id
from cart_app.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from orders.models import Payment, PaymentMethod, Order, OrderProduct
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from wallet.models import Wallet,WalletTransaction
from store.models import Wishlist,WishlistItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password








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
        
        print("yessssssssssssssssssssssssss")
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
            user = request.user
            user_wallet = Wallet.objects.create(user = user,balance = 0)
            user_wallet.save()
            # user = request.user.id

            Wishlist.objects.create(user = customer)
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



                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                    if is_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)

                        for item in cart_items:
                            item.user = user_details
                            item.save()
                except:
                    pass

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
@never_cache

def userhome(request):
    products = Product.objects.filter(is_available=True)
    # product_variants = Product_Variant.objects.filter(is_active=True)

    products_list = list()
    p = Product_Variant.objects.all()
    for pro in products:
        variants = Product_Variant.objects.filter(is_active=True,product=pro.id)
        print(pro.id)
        for variant in variants:
            products_list.append(variant)
            break


    # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active = True)  # Filter out products with no brand and inactive brands
    context = {
        'products_list':products_list
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

@login_required
@never_cache
def profile_details(request):


        # get the image from the frontent and save it to the userimage table and send the response here
    user = request.user
    print(user)
    try:
        profile = UserImage.objects.get(user = user)
    except ObjectDoesNotExist:
        profile = UserImage.objects.create(user=user)
        

    # return render(request, 'user_addresses.html', {'user_addresses': dummy_addresses})


    return render(request,'userside/profile-details.html',{'profile':profile})
        




def account_settings(request):
    return render(request,'')
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_address(request):
    user = request.user
    user_addresses = Address.objects.filter(account=user)
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'userside/profile-address.html', context)


@login_required
@never_cache
def profile_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user).order_by("-created_at")
    order_products = []

    for order in orders:
        order_products.append(OrderProduct.objects.filter(order=order))

    # Now let's print the payment method for each order
    for order in orders:
        if order.payment:
            print(order.payment.payment_method.method_name)
        else:
            print("No payment found for order #", order.order_number)
    
    paginator = Paginator(orders,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    

    context = {
        'orders': paged_products,
        'order_products': order_products
    }
    return render(request, 'userside/profile-orders.html', context)

@login_required
@never_cache
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


@login_required
@never_cache
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

@login_required
@never_cache
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

@never_cache
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

@login_required
@require_POST
def upload_profile_image(request):
    user = request.user

    try:
        user_image = UserImage.objects.get(user=user)
    except ObjectDoesNotExist:
        user_image = UserImage(user=user)

    user_image.image = request.FILES.get('image')
    user_image.save()

    return JsonResponse({'message': 'Image uploaded successfully'})


from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# User = get_user_model()

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email)
            randomotp = str(random.randint(1000, 9999))
            request.session['otp_key'] = randomotp
            request.session['email'] = email
            request.session.modified = True
            request.session.set_expiry(300)

            # Save new password to session
            request.session['password'] = passw

            subject = "Verify Your One-Time Password (OTP) - Time Gallery Ecommerce Store"
            sendermail = "timegalleryt.com"
            otp = f"Hello,\n\nYour One-Time Password (OTP) for verification at Time Gallery Ecommerce Store is: {randomotp}\n\nThank you for choosing Time Gallery Ecommerce Store.\n\nBest regards,\nTime Gallery Ecommerce Store Team"

            send_mail(subject, otp, sendermail, [email], fail_silently=True)

            return render(request, 'userside/forgot_otp.html')
        except User.DoesNotExist:
            messages.error(request, "Email does not exist")
            return redirect("user_app:forgot_password")

    return render(request, 'userside/forgotpassword.html')


def forgot_password_otp(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_app:dashboard')
        return redirect('user_app:userhome')

    email = request.session.get('email')
    password = request.session.get('password')
    print("email",email)
    print("password",password)
    print("type of passsword",type(password))


    if request.method == 'POST':
        if str(request.session['otp_key']) == str(request.POST['otp']):
            try:
                user = User.objects.get(email=email)
                new_password = password  # Change this to a known password
                hashed_password = make_password(new_password)
                print("before user password and hashed passwoed",user.password,hashed_password)
                user.password = hashed_password
                user.save()
                print("after user password",user.password)

                messages.success(request,"Password updated successfully.")
                return redirect("user_app:login")
            except User.DoesNotExist:
                print("User does not exist")
                return redirect('user_app:forgot_password_otp')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('user_app:forgot_password_otp')

    return render(request, 'userside/forgot_otp.html')


