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

    total_with_orginal_price =0
    current_user = request.user
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

    }

    return render(request,'userside/user_orders/order_summary.html',context)



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


# @login_required
# def checkout_payment_cod(request):
    # current_user = request.user
    # try:

    #     cart_items = CartItem.objects.filter(user=current_user)
    # except:
    #     return redirect('cart_app:cart')


    # if request.method == "POST":
    #     opt_id = request.POST.get('payment_option')
    #     option = PaymentMethod.objects.get(id=opt_id)
    #     option_name = option.method_name
    #     if option:
            # Assuming 'cod' is the ID of the Cash on Delivery method
            # if option_name == 'CASH ON DELIVERY':
            #     return redirect('order_app:place_order_cod')
            # elif option_name == "razorpay":
            #     return redirect('')

        # else:
        #     return HttpResponse("Something went wrong")

    # payment = PaymentMethod.objects.all()
    # context = {
    #     "payment": payment
    # }
    # return render(request, 'userside/user_orders/payment_options.html', context)
from django.http import QueryDict

# @csrf_exempt
@login_required
def checkout_payment(request):
    current_user = request.user
    
    try:
        cart_items = CartItem.objects.filter(user=current_user)
    except:
        return redirect('cart_app:cart')
    
    if request.method == "POST":
        print("request.body   :",request.body)
        data = json.loads(request.body)
        selected_payment_method = data.get('selected_payment_method')
        
        # You can add your logic here based on the selected payment method
        if selected_payment_method == 'RAZORPAY':
            total = 0
            cart_items = CartItem.objects.filter(user=current_user)
            for cart_item in cart_items:
                total += cart_item.subtotal()
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
    payment = PaymentMethod.objects.all()
    context = {
        "payment": payment
    }
    return render(request, 'userside/user_orders/payment_options.html', context)
