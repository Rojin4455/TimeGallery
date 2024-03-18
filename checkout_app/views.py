from django.shortcuts import get_object_or_404, render,redirect
from user_app.models import Address
from cart_app.models import Cart,CartItem
from cart_app.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from orders.models import PaymentMethod,Payment
from store.models import Product_Variant
from django.contrib import messages
import razorpay
from First_Ecommerce import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from admin_app.models import User
from wallet.models import Wallet,WalletTransaction
from store.models import Coupon,UserCoupon
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.utils import timezone






@login_required
def checkout_address(request):
    user = request.user
    addresses = Address.objects.filter(account=user)
    context = {
        'addresses': addresses
    }

    return render(request,'userside/user_orders/address_selection.html',context)

@login_required
def checkout_edit_address(request, id):
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

        return redirect('checkout_app:checkout_address')

    context = {
        'address': address
    }
    return render(request, 'userside/user_orders/checkout_address_edit.html', context)

@login_required
def checkout_create_address(request):

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

        return redirect('checkout_app:checkout_address')

    return render(request,'userside/user_orders/checkout_address_create.html')

@login_required
def order_summary(request, total=0, quantity=0, cart_items=None):
    current_user = request.user.id
    if 'discount' in request.session:
        
        coupon_discount = int(request.session['discount'])
        print("coupon_discount in order summary",coupon_discount)
        coupens = Coupon.objects.filter(is_expired = False)
        total_with_orginal_price =0
        user = User.objects.get(id = current_user)
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity


        discount = total_with_orginal_price - total
        total -= coupon_discount

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            # 'grand_total':grand_total,
            'discount':discount,
            'total_with_orginal_price':total_with_orginal_price,
            'coupens':coupens,
            'coupon_discount':coupon_discount,
        }

        return render(request,'userside/user_orders/order_summary.html',context)

    coupens = Coupon.objects.filter(is_expired = False,is_active=True)
    total_with_orginal_price =0
    # user_id = request.session.get('_auth_user_id')
    user = User.objects.get(id = current_user)
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    for cart_item in cart_items:
        total += cart_item.subtotal()
        total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity

 
    discount = total_with_orginal_price - total
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        # 'grand_total':grand_total,
        'discount':discount,
        'total_with_orginal_price':total_with_orginal_price,
        'coupens':coupens,
    }

    return render(request,'userside/user_orders/order_summary.html',context)





@require_POST
def apply_coupon(request):

    print("its checkout function")
    discount_amount = 0 
    if 'discount' in request.session:
        del request.session['discount']

    if discount_amount == 0 :
        print("DDDDDDDDDDDDDDDDDD")
        data = json.loads(request.body)
        coupon_code = data.get('coupencode')
        coupn_dict = {'coupon':coupon_code,}
        cache.set('coupon_code',coupn_dict )
        # grand_total = float(request.session.get('grandtotal'))
        # print('grandd',grand_total)
    
        try:
            # Attempt to get the Coupon object based on the provided coupon code
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            request.session['coupon_code'] = coupon_code
        except Coupon.DoesNotExist:
            # Handle the case where the coupon does not exist
            data = {'error': 'Coupon does not exist'}
            return JsonResponse(data, status=200)
        
        try:
            # Attempt to get the UserCoupon object for the current user and coupon
            cart_item_instance= CartItem.objects.filter(user=request.user)
            for i in cart_item_instance:
                i.cart.id
            total = 0
            print(cart_item_instance)
            for cart_item in cart_item_instance:
                total += cart_item.subtotal()
            total = int(total)
            cart_instance = Cart.objects.get(id=i.cart.id)   
            coupon_usage, created = UserCoupon.objects.get_or_create(
            coupon=coupon,
            user=request.user,
            defaults={'usage_count': 0}  # Set default values for newly created instance
            )
            print("coupon usage count",coupon_usage.usage_count)

            cart_instance.coupon = coupon_usage
            cart_instance.save()

        except UserCoupon.DoesNotExist:
            # Handle the case where the UserCoupon does not exist
            data = {'error': 'UserCoupon does not exist'}
            return JsonResponse(data, status=200)
        
        discount=coupon.discount_percentage
        if coupon_usage.apply_coupon() and total >= float(coupon.minimum_amount):


            discount_amount = (discount / 100) * total
            coupon.total_coupons -= 1
            coupon.save()
            total -= discount_amount
            request.session['discount'] = discount_amount 
            print(" request.session['discount']", request.session['discount'])
            print("coupon code",coupon_code)
            data={'discount_amount':discount_amount,'discount':discount,'success':'Coupon Applied','total':total,'coupon_code':coupon_code}
            print(data,'3')
            return JsonResponse(data,status=200)
            
        else:

            if coupon.expire_date < timezone.now().date():
                data={'error':'Coupon expired'}
                print("1")
                print('Failed')
                return JsonResponse(data)
            elif total < float(coupon.minimum_amount):
                data={'error':'Minimum amount required'}
                print("2")

                print('Failed')
                return JsonResponse(data)
            elif coupon.total_coupons == 0:
                data={'error':'Coupon not available'}
                print("3")

                print('Failed')
                return JsonResponse(data)
            data={'error':'Maximum uses of the coupon reached'}
            print("4")
            print('Failed')
            return JsonResponse(data,status=500)
        
    else:
        print("FFW")
        return JsonResponse({'error': 'Coupon already applied'})



def remove_order_summary(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, user=current_user)
    else:
        
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity>1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('checkout_app:order_summary')


def update_order_summary(request,product_id):

    product = get_object_or_404(Product_Variant,id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        # cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, user=current_user)
    else:
        
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity < product.stock:

        cart_item.quantity += 1
        cart_item.save()
        return redirect('checkout_app:order_summary')
    else:
        messages.error(request,'Stock Limit Exceeded')
        return redirect('checkout_app:order_summary')
    



def remove_order_summary_item(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=current_user)

    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('checkout_app:order_summary')




@login_required
def checkout_payment(request,total=0,total_with_og_price=0,discount=0):
    current_user = request.user
    
    try:
        cart_items = CartItem.objects.filter(user=current_user)
        for cart_item in cart_items:
            total += cart_item.subtotal()
    except:
        return redirect('cart_app:cart')
    
    if "discount" in request.session:
        print("request.session['discount']",request.session['discount'])
        coupon_discount = request.session['discount']
        total = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
        # print("Total",type(intfloat(total)))
        rounded_total = round(total)
        total = int(rounded_total)
        coupon_discount = int(coupon_discount)
        total -= coupon_discount

        print("int total",total)
        
        if request.method == "POST":
            print("request.body   :",request.body)
            data = json.loads(request.body)
            selected_payment_method = data.get('selected_payment_method')
            
            # You can add your logic here based on the selected payment method
            if selected_payment_method == 'RAZORPAY':
                # total = 0
                # cart_items = CartItem.objects.filter(user=current_user)
                # for cart_item in cart_items:
                #     total += cart_item.subtotal()
                total_amount = int(total * 100)  # Replace with your actual total amount calculation
                print("total amount:  ",total_amount)
                currency = "INR"  # Replace with your currency
                order_data = {
                    'amount': total_amount,
                    'currency': currency,
                    'receipt': 'order_rcptid_11',  # Replace with your receipt ID or generate dynamically
                    'payment_capture': 1  # Auto-capture payment
                }
                
                client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
                order = client.order.create(data=order_data)
                order_id = order['id']
                payment_methods_instance = PaymentMethod.objects.get(method_name="RAZORPAY")
                payment = Payment.objects.create(
                    user = current_user,
                    payment_method = payment_methods_instance,
                    payment_order_id = order_id,
                    amount_paid = 0,
                    payment_status = 'PENDING',
                )
                
                
                # Create context for rendering the payment template
                context = {
                    'order_id': order['id'],
                    'amount': order['amount'],
                    'currency': order['currency'],
                    'key_id': settings.RAZOR_PAY_KEY_ID
                }
                
                # Return JSON response with context data for client-side handling
                return JsonResponse({'context': context})
                
            elif selected_payment_method == 'CASH_ON_DELIVERY':
                # Your logic for Cash on Delivery
                return redirect('order_app:place_order_cod')
                
            else:
                # Handle other payment methods or errors
                return JsonResponse({'error': 'Invalid payment method'})
        
        # If GET request or other conditions, render the payment options template
            
        user = request.user.id
        user_instence = User.objects.get(id = user)
        print(user_instence.username)
        wallet = Wallet.objects.get(user = user_instence)
        print(" wallet balance: ",wallet.balance)
        payment = PaymentMethod.objects.all()
        context = {
            "payment": payment,
            "wallet_balance":wallet.balance,
            "coupon_discount":coupon_discount,
            "total":total,
        }
    else:
        print("YUIDASHGFUHGFDIUW")
        if request.method == "POST":
            print("request.body www  :",request.body)
            data = json.loads(request.body)
            selected_payment_method = data.get('selected_payment_method')
            
            # You can add your logic here based on the selected payment method
            if selected_payment_method == 'RAZORPAY':
                # total = 0
                # cart_items = CartItem.objects.filter(user=current_user)
                # for cart_item in cart_items:
                #     total += cart_item.subtotal()
                total_amount = int(total * 100)  # Replace with your actual total amount calculation
                print("total amount:  ",total_amount)
                currency = "INR"  # Replace with your currency
                order_data = {
                    'amount': total_amount,
                    'currency': currency,
                    'receipt': 'order_rcptid_11',  # Replace with your receipt ID or generate dynamically
                    'payment_capture': 1  # Auto-capture payment
                }
                
                client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
                order = client.order.create(data=order_data)
                order_id = order['id']
                payment_methods_instance = PaymentMethod.objects.get(method_name="RAZORPAY")
                payment = Payment.objects.create(
                    user = current_user,
                    payment_method = payment_methods_instance,
                    payment_order_id = order_id,
                    amount_paid = 0,
                    payment_status = 'PENDING',
                )
                
                
                # Create context for rendering the payment template
                context = {
                    'order_id': order['id'],
                    'amount': order['amount'],
                    'currency': order['currency'],
                    'key_id': settings.RAZOR_PAY_KEY_ID
                }
                
                # Return JSON response with context data for client-side handling
                return JsonResponse({'context': context})
                
            elif selected_payment_method == 'CASH_ON_DELIVERY':
                # Your logic for Cash on Delivery
                return redirect('order_app:place_order_cod')
                
            else:
                # Handle other payment methods or errors
                return JsonResponse({'error': 'Invalid payment method'})
        
        # If GET request or other conditions, render the payment options template
            
        user = request.user.id
        user_instence = User.objects.get(id = user)
        print(user_instence.username)
        wallet = Wallet.objects.get(user = user_instence)
        print(" wallet balance: ",wallet.balance)
        payment = PaymentMethod.objects.all()
        context = {
            "payment": payment,
            "wallet_balance":wallet.balance,
        }
    return render(request, 'userside/user_orders/payment_options.html', context)
