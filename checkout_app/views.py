from django.shortcuts import get_object_or_404, render,redirect
from user_app.models import Address
from cart_app.models import Cart,CartItem
from cart_app.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist




def checkout_address(request):
    user = request.user
    addresses = Address.objects.filter(account=user)
    context = {
        'addresses': addresses
    }

    return render(request,'userside/user_orders/address_selection.html',context)


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


def order_summary(request, total=0, quantity=0, cart_items=None):

    total_with_orginal_price =0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass


    
    discount = total_with_orginal_price - total

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        # 'grand_total':grand_total,
        'discount':discount,
        'total_with_orginal_price':total_with_orginal_price,


    }

    return render(request,'userside/user_orders/order_summary.html', context)




def checkout_payment(request):
    return render(request,'userside/user_orders/payment_options.html')

def order_success(request):
    return render(request,'userside/user_orders/order-success.html')