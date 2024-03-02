from django.shortcuts import render
from .models import Payment,PaymentMethod,Order,OrderProduct
from user_app.models import Address
from admin_app.models import User
from cart_app.models import Cart,CartItem

# Create your views here.

def place_order_cod(request):
    

    user_id = request.user.id

    # Get necessary instances
    
    payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")

    user_instance = User.objects.get(id=user_id)

    address = Address.objects.get(is_default=True, account=user_instance)

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)

    total_with_original_price = 0
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += cart_item.subtotal()
        total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity
    grand_total = total



    # Create ShippingAddress instance
    address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]
    
    

    # Create Payment instance
    payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')
    
    
    draft_order= Order.objects.create(
            user=user_instance,
            shipping_address=address1,
            order_total=grand_total,
            is_ordered  = True,
        )
    for cart_item in cart_items:
        product= cart_item.product
        product.stock -= cart_item.quantity
        product.save()
        
    for cart_item in cart_items:
            OrderProduct.objects.create(
                order           = draft_order,
                user            = user_instance,
                product_variant = cart_item.product.get_product_name(),
                quantity        = cart_item.quantity,
                product_price   = float(cart_item.product.sale_price),
                images          = cart_item.product.thumbnail_image,
                ordered         = True,
            )
            print(cart_item.product.get_product_name())

    cart_items.delete()    
    
    order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
    for i in order_dtails:
        address=i.order.shipping_address


    return render(request,'userside/user_orders/order-success.html')