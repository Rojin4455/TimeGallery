from django.shortcuts import render,redirect
from .models import Payment,PaymentMethod,Order,OrderProduct
from user_app.models import Address
from admin_app.models import User
from cart_app.models import Cart,CartItem
from django.http import JsonResponse
from django.http import HttpResponse
from store.models import Product_Variant
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import razorpay
from First_Ecommerce import settings
from django.contrib.auth.decorators import login_required




# Create your views here.

def place_order_cod(request):
    

    user_id = request.user.id

    # Get necessary instances
    
    payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")

    user_instance = User.objects.get(id=user_id)

    address = Address.objects.get(is_default=True, account=user_instance)

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    
    for i in cart_items:
        if i.product.stock < 1:
            messages.error(request,"Product Variant is Out Of Stock")
            return redirect('checkout_app:checkout_payment')

    total = 0
    quantity = 0
    total_with_orginal_price = 0

    for cart_item in cart_items:
        total += cart_item.subtotal()
        total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity

    discount = total_with_orginal_price - total


    # Create ShippingAddress instance
    address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]
    
    

    # Create Payment instance
    payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')
    
    
    draft_order= Order.objects.create(
            user=user_instance,
            shipping_address=address1,
            order_total=total,
            is_ordered  = True,
            payment = payment,
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
                product_id      = cart_item.product.id,
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
    
    print("address: ",address)

    cleaned_string = address.replace('[', '').replace(']', '')


    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]
    print(cleaned_data)
    str1 = str()
    k = 1
    for i in cleaned_data:
        if k == 1:
            str1+=i
        else:
            str1+=" "+i
        k = 2

    str1 = str1.replace(","," ")
    print(str1)
         

    draft_order.shipping_address = str1
    draft_order.save()
    print('order_dtails: ',draft_order)
    print("address: ",str1)
    print('order_product:  ',order_dtails)
    
    context = {
                'order_dtails' : draft_order,
                'address' : str1,
                'order_product' : order_dtails,
                'grand_total':total,
                'total_with_orginal_price':total_with_orginal_price,
                'discount':discount,
                }

    return render(request,'userside/user_orders/order-success.html',context)



def profile_order_details(request, id):
     
     order = Order.objects.get(id = id)

     order_products = OrderProduct.objects.filter(order=order)
     print("product_details order",order.id)
     context = {
          'order_dtails':order,
          'order_products':order_products,
     }
     
     return render(request,'userside/user_orders/profile-order-details.html', context)



def cancel_product(request, item_id):
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product.order_status = "Cancelled User"
    ordered_product.grand_totol = 0
    ordered_product.save()
    ordered_product_quantity = ordered_product.quantity

    product_id = ordered_product.product_id
    product_variant = Product_Variant.objects.get(id = product_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()

    order = ordered_product.order
    order_products = OrderProduct.objects.filter(order = order)
    order = Order.objects.get(id = order.id)
    order.order_total -= ordered_product.grand_totol

    print("ordered_product.grand_totol:  ",ordered_product.grand_totol)
    print("order.order_total:  ",order.order_total)

    order.save()
    print("ordered Products:  ",order_products)
    print("order :",order)
    
    return redirect("order_app:profile_order_details", order.id)


def return_product(request,item_id):
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product.order_status = "Returned User"
    ordered_product.grand_totol = 0
    ordered_product.save()
    ordered_product_quantity = ordered_product.quantity

    product_id = ordered_product.product_id
    product_variant = Product_Variant.objects.get(id = product_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()


    order = ordered_product.order
    order_products = OrderProduct.objects.filter(order = order)
    order = Order.objects.get(id = order.id)
    order.order_total -= ordered_product.grand_totol

    order.save()


    return redirect("order_app:profile_order_details", order.id)


@csrf_exempt
def place_order_razpay(request):


    if request.method == "POST":
        try:
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')
            print(f'1:{payment_id},2:{razorpay_order_id},3:{signature}')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
            result = client.utility.verify_payment_signature(params_dict)
            
            if not result :
                return redirect('order_app:paymentfail')
            else:
                return redirect('order_app:order_success',razorpay_order_id,payment_id,signature)

        except Exception as e:
            print('Exception:', str(e))
            # return HttpResponseBadRequest()
            return redirect('order_app:paymentfail')
    else:
        return redirect('checkout_app:checkout_payment')





def order_success(request, razorpay_order_id,payment_id,signature):

    payment = Payment.objects.get(payment_order_id=razorpay_order_id)
                
    payment.payment_status = 'SUCCESS'
    payment.payment_id = payment_id
    payment.payment_signature = signature
    # order = payment.order.get()
    user = payment.user
    total = 0
    total_with_orginal_price = 0
    quantity = 0
    discount = 0
    cart_items = CartItem.objects.filter(user=user)
    for cart_item in cart_items:
        total += cart_item.subtotal()
        total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity

    discount = total_with_orginal_price - total
    payment.amount_paid = total
    payment.save()


    address = Address.objects.get(is_default=True, account=user)
    address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]

    draft_order= Order.objects.create(
            user=user,
            shipping_address=address1,
            order_total=total,
            is_ordered  = True,
            payment = payment,
        )
    for cart_item in cart_items:
        product= cart_item.product
        product.stock -= cart_item.quantity
        product.save()


    for cart_item in cart_items:
        OrderProduct.objects.create(
        order           = draft_order,
        user            = user,
        product_variant = cart_item.product.get_product_name(),
        product_id      = cart_item.product.id,
        quantity        = cart_item.quantity,
        product_price   = float(cart_item.product.sale_price),
        images          = cart_item.product.thumbnail_image,
        ordered         = True,
    )
    print(cart_item.product.get_product_name())

    cart_items.delete()    

    order_dtails=OrderProduct.objects.filter(user=user,order=draft_order)
    for i in order_dtails:
        address=i.order.shipping_address

    print("address: ",address)

    cleaned_string = address.replace('[', '').replace(']', '')
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]
    print(cleaned_data)
    str1 = str()
    k = 1
    for i in cleaned_data:
        if k == 1:
            str1+=i
        else:
            str1+=" "+i
        k = 2

    str1 = str1.replace(","," ")
    print(str1)
            

    draft_order.shipping_address = str1
    draft_order.save()    




    draft_order.shipping_address = str1
    draft_order.save()
    print('order_dtails: ',draft_order)
    print("address: ",str1)
    print('order_product:  ',order_dtails)
    
    context = {
                'order_dtails' : draft_order,
                'address' : str1,
                'order_product' : order_dtails,
                'grand_total':total,
                'total_with_orginal_price':total_with_orginal_price,
                'discount':discount,
                }
    print('working ijgrfuhgf')
    return render(request, 'userside/user_orders/order-success.html', context)



def paymentfail(request):

    return render(request, 'userside/user_orders/paymentfail.html')




