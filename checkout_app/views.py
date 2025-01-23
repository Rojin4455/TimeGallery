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
from decimal import Decimal







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

        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.phone_number = request.POST.get('phone_number')
        address.street_address = request.POST.get('street_address')
        address.town_city = request.POST.get('town_city')
        address.state = request.POST.get('state')
        address.country_region = request.POST.get('country_region')
        address.zip_code = request.POST.get('zip_code')
        address.save()


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

        user=request.user
        address = Address.objects.create(account=user,first_name=first_name,last_name=last_name,phone_number=phone_number,town_city=town_city,street_address=street_address,state=state,country_region=country_region,zip_code=zip_code)
        make_default = request.POST.get('make_default')
        is_default = make_default == 'on'
        address.is_default = is_default
        address.save()

        return redirect('checkout_app:checkout_address')

    return render(request,'userside/user_orders/checkout_address_create.html')

@login_required
def order_summary(request, total=0, quantity=0, cart_items=None):

    current_user = request.user.id
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.id
    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)

    if cart.coupon_applied != None:

        total_with_orginal_price = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
        discount = total_with_orginal_price - total
        total -= cart.coupon_discount
        coupens = Coupon.objects.filter(is_expired = False)
        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'discount':discount,
            'total_with_orginal_price':total_with_orginal_price,
            'coupens':coupens,
            'coupon_discount':cart.coupon_discount,
        }
        return render(request,'userside/user_orders/order_summary.html',context)
    else:
        total_with_orginal_price = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
        coupens = Coupon.objects.filter(is_expired = False)
        discount = total_with_orginal_price - total

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'discount':discount,
            'total_with_orginal_price':total_with_orginal_price,
            'coupens':coupens,
        }
        return render(request,'userside/user_orders/order_summary.html',context)

@require_POST
@login_required
def apply_coupon(request):
    if request.method == "POST":
        discount_amount = 0 

        data = json.loads(request.body)
        coupon_code = data.get('coupencode')


        try:
            # Attempt to get the Coupon object based on the provided coupon code
            coupon = Coupon.objects.get(coupon_code=coupon_code)

            if coupon.is_expired == False:
                cart_item_instance= CartItem.objects.filter(user=request.user).first()
                cart_item_id = cart_item_instance.id
                cart_item = CartItem.objects.get(id = cart_item_id)
                try:

                    cart = Cart.objects.get(cart_id=cart_item.cart)
                except Exception as e:
                    
                    print("exception cart",str(e))

                cart.coupon_applied = coupon
                cart_item_instance= CartItem.objects.filter(user=request.user)
                total = 0
                for cart_item in cart_item_instance:
                    total += cart_item.subtotal()
                total = Decimal(total)

                coupon_discount = Decimal(coupon.discount_percentage)
                discount_amount = (total * coupon_discount) / Decimal(100)
                total_after_discount = total - discount_amount



                try:
                    user_coupon = UserCoupon.objects.get(coupon = coupon, user = request.user)
                except Exception as e:
                    
                    print("exception usercoupon",str(e))
                    user_coupon = UserCoupon.objects.create(user = request.user, coupon = coupon, usage_count = 0)
                if user_coupon.apply_coupon() and total >= float(coupon.minimum_amount):
                    cart.coupon_discount = int(discount_amount)
                    cart.save()
                    request.session['coupon_code'] = coupon_code
                    data={'discount_amount':discount_amount,'discount':coupon.discount_percentage,'success':'Coupon Applied','total':total_after_discount,'coupon_code':coupon_code}
                    return JsonResponse(data,status=200)
                else:
                    if coupon.expire_date < timezone.now().date():
                        data={'error':'Coupon expired'}

                        return JsonResponse(data)
                    elif total < float(coupon.minimum_amount):
                        data={'error':'Minimum amount required'}

                        return JsonResponse(data)
                    elif coupon.total_coupons == 0:
                        data={'error':'Coupon not available'}

                        return JsonResponse(data)
                    
                    elif user_coupon.apply_coupon() == False:
                        data={'error':'Maximum Uses Reached'}
                        return JsonResponse(data)


                    data={'error':'Maximum uses of the coupon reached'}

                    return JsonResponse(data,status=500)


            else:
                data = {'error': 'Coupon is Expired'}
                return JsonResponse(data, status=200)       
        except Coupon.DoesNotExist:
            # Handle the case where the coupon does not exist
            data = {'error': 'Coupon does not exist'}
            return JsonResponse(data, status=200)
    

def cancel_coupon(request):
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.id
    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)
    cart.coupon_discount = 0
    cart.coupon_applied = None
    cart.save()
    messages.success(request,"coupen deleted")
    return redirect("checkout_app:order_summary")

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
def checkout_payment(request,total=0,total_with_og_price=0,discount=0,quantity=0):

    current_user = request.user
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.id
    cart_item = CartItem.objects.get(id = cart_item_id)
    wallet = Wallet.objects.get(user = current_user)
    payment = PaymentMethod.objects.all()

    cart = Cart.objects.get(cart_id=cart_item.cart)
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    print("NOT NOTE")
    if cart.coupon_applied != None:
        print("yesssssssssssssssssss")
        print("coupon applied")
        print(cart.coupon_discount)
        total_with_orginal_price = 0


        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        discount = total_with_orginal_price - total
        total -= cart.coupon_discount
        context1 = {
            "payment": payment,
            "wallet_balance":wallet.balance,
            "coupon_discount":cart.coupon_discount,
            "total":total,
            
        }
    else:
        total_with_orginal_price = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
        # coupens = Coupon.objects.filter(is_expired = False)
        # discount = total_with_orginal_price - total

        context1 = {
            "payment": payment,
            "wallet_balance":wallet.balance,
            "total":total,
        }

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
            currency = "INR" 
            order_data = {
                'amount': total_amount,
                'currency': currency,
                'receipt': 'order_rcptid_11',
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
            
        # user = request.user.id
        # user_instence = User.objects.get(id = user)
        # print(user_instence.username)
        # wallet = Wallet.objects.get(user = user_instence)
        # print(" wallet balance: ",wallet.balance)
        # payment = PaymentMethod.objects.all()
        # context = {
        #     "payment": payment,
        #     "wallet_balance":wallet.balance,
        #     "coupon_discount":coupon_discount,
        #     "total":total,
        # }
                
            # else:
                # Handle other payment methods or errors
                # return JsonResponse({'error': 'Invalid payment method'})
    context1["BASE_API_URL"] = settings.BASE_API_URL
    return render(request, 'userside/user_orders/payment_options.html', context1)
    # try:
    #     cart_items = CartItem.objects.filter(user=current_user)
    #     for cart_item in cart_items:
    #         total += cart_item.subtotal()
    # except:
    #     return redirect('cart_app:cart')
    
    # if "discount" in request.session:
    #     print("request.session['discount']",request.session['discount'])
    #     coupon_discount = request.session['discount']
    #     total = 0
    #     for cart_item in cart_items:
    #         total += cart_item.subtotal()
    #     for i in cart_items:
    #         if i.product.stock < 1:
    #             messages.error(request,"Product Variant is Out Of Stock")
    #             return redirect('checkout_app:checkout_payment')
    #     # print("Total",type(intfloat(total)))
    #     rounded_total = round(total)
    #     total = int(rounded_total)
    #     coupon_discount = int(coupon_discount)
    #     total -= coupon_discount

    #     print("int total",total)
        
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
                for i in cart_items:

                    if i.product.stock < 1:
                        messages.error(request,"Product Variant is Out Of Stock")
                        return redirect('checkout_app:checkout_payment')
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
