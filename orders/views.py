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
from wallet.models import Wallet,WalletTransaction
from store.models import Coupon,UserCoupon
from django.db.models import Q



# Create your views here.
@login_required
def place_order_cod(request):

    user_id = request.user.id

    # Get necessary instances
    
    payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")

    user_instance = User.objects.get(id=user_id)

    address = Address.objects.get(is_default=True, account=user_instance)

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.pk

    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)

    if cart.coupon_applied != None:
        total_with_orginal_price = 0

        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
    
        coupon_code = request.session['coupon_code']
        del  request.session['coupon_code']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 
    
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
        total1 = total
        total1 -= cart.coupon_discount


        # Create ShippingAddress instance
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]



        # Create Payment instance
        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')


        draft_order= Order.objects.create(
                user=user_instance,
                shipping_address=address1,
                order_total=total,
                additional_discount = discount,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total1,
                coupon_discount = cart.coupon_discount
            )

        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        try:
            disc_per = cart.coupon_discount/len(cart_items)

        except ZeroDivisionError:
            messages.error(request,"product is empty")
            return redirect("order_app:paymentfail")
        
        for cart_item in cart_items:
                o = OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )
                o.save()
                o.grand_totol -= disc_per
                o.save()

        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address

        cleaned_string = address.replace('[', '').replace(']', '')


        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()
        total -= cart.coupon_discount
        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':total,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    'coupon_discount':cart.coupon_discount,
                    }
    else:
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
                additional_discount = discount,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total
            )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        # disc_per = coupon_discount/len(cart_items)
        for cart_item in cart_items:
                o = OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )
                o.save()


        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')


        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()


        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':total,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    }
    return render(request,'userside/user_orders/order-success.html',context)




@login_required
def profile_order_details(request, id):
    order = Order.objects.get(id = id)
    order_products1 = OrderProduct.objects.filter(order = order)
    order_products_deliverd = OrderProduct.objects.filter(order = order,order_status = "Delivered")
    
    
    order_products = OrderProduct.objects.filter(order = order).first()
    product_ispaid = True
    if len(order_products1) == len(order_products_deliverd):
        product_ispaid1 = True
    else:
        product_ispaid1 = False
    for i in order_products1:
        if i.is_paid == False:
            product_ispaid = False
    # if order_products.grand_totol < order_products.product_price:
    if order.order_grandtotal < order.order_total:
        
        order_actual_total = 0
        for i in order_products1:
            order_actual_total += i.product_price
        

        context = {
                'order_dtails':order,
                'order_products':order_products1,
                'product_total':order.order_total,
                'coupon_discount':order.coupon_discount,
                'grand_total':order.order_grandtotal,
                'product_ispaid':product_ispaid1
            }
    else:
        context = {
            'order_dtails':order,
            'order_products':order_products,
            'order_products':order_products1,
            'grand_total':order.order_grandtotal,
            "product_ispaid":product_ispaid1,
        }

    return render(request,'userside/user_orders/profile-order-details.html', context)



@login_required
def cancel_product(request, item_id):
    coupon_discount_pro = 0
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product_quantity = ordered_product.quantity

    order = Order.objects.get(id=ordered_product.order.id)
    product_id = ordered_product.product_id
    product_variant = Product_Variant.objects.get(id = product_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()

    ordered_product.order_status = "Cancelled User"
    ordered_product.save()


    payment_method = PaymentMethod.objects.get(method_name = order.payment.payment_method.method_name)


    if payment_method.method_name != "CASH ON DELIVERY":
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance+= ordered_product.grand_totol
        wallet.save()

        WalletTransaction.objects.create(wallet = wallet,transaction_type = "CREDIT", transaction_detail = "Order Cancelled", amount = ordered_product.grand_totol)
    
    return redirect("order_app:profile_order_details", order.id)


@login_required
def return_product(request,item_id):
    coupon_discount_pro = 0
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product.order_status = "Returned User"
    ordered_product.save()

    order = Order.objects.get(id=ordered_product.order.id)

    product_id = ordered_product.product_id
    product_variant = Product_Variant.objects.get(id = product_id)
    product_variant.stock += ordered_product.quantity
    product_variant.save()


    wallet = Wallet.objects.get(user=request.user)
    wallet.balance+= ordered_product.grand_totol
    wallet.save()


    WalletTransaction.objects.create(wallet = wallet,transaction_type = "CREDIT", transaction_detail = "Order Returned", amount = ordered_product.grand_totol)


    return redirect("order_app:profile_order_details", order.id)


@csrf_exempt
def place_order_razpay(request):


    if request.method == "POST":
        try:
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')

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
            return redirect('order_app:payment_fail_order')
    else:
        messages.error(request,"Payment is Faied, Try Again")
        return redirect('checkout_app:checkout_payment')
    

def payment_fail_order(request):

    payment_method = PaymentMethod.objects.get(method_name = "RAZORPAY")
    payment = Payment.objects.create(
        user = request.user,
        payment_status = 'FAILED',
        payment_method = payment_method,
        amount_paid = 0,
        is_paid = False,
    )

    user = payment.user
    total = 0
    total_with_orginal_price = 0
    quantity = 0
    discount = 0

    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.pk

    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)

    if cart.coupon_applied != None:
        coupon_code = request.session['coupon_code']
        del request.session['coupon_code']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 
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
        total1 = total - cart.coupon_discount



        address = Address.objects.get(is_default=True, account=user)
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]

        draft_order= Order.objects.create(
                user=user,
                shipping_address=address1,
                order_total=total,
                is_ordered  = False,
                payment = payment,
                additional_discount = discount,
                order_grandtotal = total1,
                coupon_discount = cart.coupon_discount
            )
        
        draft_order.save()
        try:
            disc_per = cart.coupon_discount/len(cart_items)

        except ZeroDivisionError:
            messages.error(request,"product is empty")
            return redirect("order_app:paymentfail")
        
        for cart_item in cart_items:
            o = OrderProduct.objects.create(
                order           = draft_order,
                user            = user,
                product_variant = cart_item.product.get_product_name(),
                product_id      = cart_item.product.id,
                quantity        = cart_item.quantity,
                product_price   = float(cart_item.product.sale_price),
                images          = cart_item.product.thumbnail_image,
                ordered         = False,
            )
            o.save()

            o.grand_totol -= disc_per

            o.save()

        order_dtails=OrderProduct.objects.filter(user=user,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address

        cleaned_string = address.replace('[', '').replace(']', '')
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()    




        draft_order.shipping_address = str1
        draft_order.save()
        
    else:
        cart_items = CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        discount = total_with_orginal_price - total



        address = Address.objects.get(is_default=True, account=user)
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]

        draft_order= Order.objects.create(
                user=user,
                shipping_address=address1,
                order_total=total,
                additional_discount = discount,
                is_ordered  = False,
                payment = payment,
                order_grandtotal = total
            )

        
        for cart_item in cart_items:
            OrderProduct.objects.create(
            order           = draft_order,
            user            = user,
            product_variant = cart_item.product.get_product_name(),
            product_id      = cart_item.product.id,
            quantity        = cart_item.quantity,
            product_price   = float(cart_item.product.sale_price),
            images          = cart_item.product.thumbnail_image,
            ordered         = False,
        )


        order_dtails=OrderProduct.objects.filter(user=user,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()    


    return redirect('checkout_app:checkout_payment')




def repay_payment(request,id):

    if request.method == 'POST':
        order = Order.objects.get(id = id)
        ordered_products = OrderProduct.objects.filter(order = order)
        payment = Payment.objects.get(id = order.payment.id)

        client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))

        payment_data = {
                'amount': int(order.order_grandtotal)*100,
                'currency': 'INR',
                'receipt': 'order_fund',  # Update as needed
                'payment_capture': 1  # Auto-capture payment
        }
        try:

            payment = client.order.create(data=payment_data)
            return JsonResponse({'success': True,'order_id': payment['id'],'amount': payment['amount'], 'product_order_id':order.id})
        except Exception as e:
            print(str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt
def repayment_handler(request):
    if request.method == "POST":
        try:

            id = request.GET.get('id', '')
            order = Order.objects.get(id = id)

            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
            result = client.utility.verify_payment_signature(params_dict)

            if not result:
                messages.error(request,"Payment Faild Try Again")

                return redirect("order_app:profile_order_details",id)
            else:
                try:

                    return redirect('order_app:repayment_success',params_dict=params_dict,id=id) 
                except Exception as e:
                    print("exception:   ",str(e))
        except Exception as e:
            print('Exception:', str(e))
            messages.error(request,"Payment Faild Try Again")

            return redirect("order_app:profile_order_details",id)
    messages.error(request,"Payment Faild Try Again")


    return redirect("order_app:profile_order_details",id)




def repayment_success(request,params_dict,id):
    import ast
    params_dict = ast.literal_eval(params_dict)
    order = Order.objects.get(id = id)
    razorpay_order_id = params_dict.get('razorpay_order_id', '')
    razorpay_payment_id = params_dict.get('razorpay_payment_id', '')
    razorpay_signature = params_dict.get('razorpay_signature', '')


    payment = Payment.objects.get(id = order.payment.id)
    payment.payment_status = "SUCCESS"
    payment.payment_signature = razorpay_signature,
    payment.amount_paid = order.order_grandtotal,
    payment.is_paid = True
    payment.payment_order_id = razorpay_order_id

    payment.save()


    ordered_products = OrderProduct.objects.filter(order = order)

    for i in ordered_products:
        i.ordered = True

    order.is_ordered =True

    for i in ordered_products:
        try:
            product = Product_Variant.objects.get(id = i.product_id)
            product.stock -= i.quantity
            product.save()
        except:
            pass
 

    messages.success(request,"Payment Completed Successfully")
    return redirect("order_app:profile_order_details",id)






@login_required
def order_success(request, razorpay_order_id,payment_id,signature):

    payment = Payment.objects.get(payment_order_id=razorpay_order_id)
                
    payment.payment_status = 'SUCCESS'
    payment.payment_id = payment_id
    payment.payment_signature = signature
    user = payment.user
    total = 0
    total_with_orginal_price = 0
    quantity = 0
    discount = 0

    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.pk

    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)

    if cart.coupon_applied != None:

        coupon_code = request.session['coupon_code']
        del request.session['coupon_code']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 
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
        total1 = total
        total1 -= cart.coupon_discount
        payment.amount_paid = total1
        payment.save()


        address = Address.objects.get(is_default=True, account=user)
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]

        draft_order= Order.objects.create(
                user=user,
                shipping_address=address1,
                order_total=total,
                is_ordered  = True,
                payment = payment,
                additional_discount = discount,
                order_grandtotal = total1,
                coupon_discount = cart.coupon_discount
            )
        
        draft_order.save()

        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        try:
            disc_per = cart.coupon_discount/len(cart_items)

        except ZeroDivisionError:
            messages.error(request,"product is empty")
            return redirect("order_app:paymentfail")
        
        for cart_item in cart_items:
            o = OrderProduct.objects.create(
                order           = draft_order,
                user            = user,
                product_variant = cart_item.product.get_product_name(),
                product_id      = cart_item.product.id,
                quantity        = cart_item.quantity,
                product_price   = float(cart_item.product.sale_price),
                images          = cart_item.product.thumbnail_image,
                ordered         = True,
            )
            o.save()

            o.grand_totol -= disc_per

            o.save()

        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()    




        draft_order.shipping_address = str1
        draft_order.save()

        
        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':total1,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    'coupon_discount':cart.coupon_discount
                    }
        return render(request, 'userside/user_orders/order-success.html', context)
    else:
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
                additional_discount = discount,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total
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

        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()    




        draft_order.shipping_address = str1
        draft_order.save()

        
        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':total,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    }
        return render(request, 'userside/user_orders/order-success.html', context)



def paymentfail(request):

    return render(request, 'userside/user_orders/paymentfail.html')




def wallet_order(request):
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    for i in cart_items:

        if i.product.stock < 1:
            messages.error(request,"Product Variant is Out Of Stock")
            return redirect('checkout_app:checkout_payment')
    current_user = request.user
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.id
    cart_item = CartItem.objects.get(id = cart_item_id)
    wallet = Wallet.objects.get(user = current_user)
    payment = PaymentMethod.objects.all()

    cart = Cart.objects.get(cart_id=cart_item.cart)
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    if cart.coupon_applied != None:

        total_with_orginal_price = 0

        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        user = request.user.id
        user_instence = User.objects.get(id = user)
        wallet = Wallet.objects.get(user = user_instence)
        amount = int(float(request.GET.get('amount', None)))
        wallet_transaction = WalletTransaction.objects.create(
                wallet = wallet,
                transaction_type = "DEBIT",
                amount = (total-cart.coupon_discount)
        )
        wallet.balance -= (total-cart.coupon_discount)
        wallet.save()
    else:
        total,quantity = 0,0
        total_with_orginal_price = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        WalletTransaction.objects.create(
            wallet = wallet,
            transaction_type = "DEBIT",
            amount = total
        )
        wallet.balance -= total
        wallet.save()

    return redirect("order_app:place_order_wallet")
    




@login_required
def place_order_wallet(request):
    

    user_id = request.user.id

    # Get necessary instances
    
    payment_methods_instance = PaymentMethod.objects.get(method_name="WALLET")

    user_instance = User.objects.get(id=user_id)

    address = Address.objects.get(is_default=True, account=user_instance)

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    cart_item_instance= CartItem.objects.filter(user=request.user).first()
    cart_item_id = cart_item_instance.pk

    cart_item = CartItem.objects.get(id = cart_item_id)

    cart = Cart.objects.get(cart_id=cart_item.cart)

    if cart.coupon_applied != None:

        total_with_orginal_price = 0

        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
    
        coupon_code = request.session['coupon_code']
        del request.session['coupon_code']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 
    
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
        total1 = total - cart.coupon_discount


        # Create ShippingAddress instance
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]



        # Create Payment instance
        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=total1,payment_status='SUCCESS')


        draft_order= Order.objects.create(
                user=user_instance,
                shipping_address=address1,
                order_total=total,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total1,
                coupon_discount = cart.coupon_discount
            )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        try:
            disc_per = cart.coupon_discount/len(cart_items)
        except ZeroDivisionError:
            messages.error(request,"product is empty")
            return redirect("order_app:paymentfail")
        for cart_item in cart_items:
                o = OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )
                o.save()
                o.grand_totol -= disc_per
                o.save()

        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')


        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()

        total -= cart.coupon_discount
        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':draft_order.order_grandtotal,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    'coupon_discount':cart.coupon_discount,
                    }
    else:
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
        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=total,payment_status='SUCCESS')


        draft_order= Order.objects.create(
                user=user_instance,
                shipping_address=address1,
                order_total=total,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total
            )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        for cart_item in cart_items:
                o = OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )
                o.save()


        cart_items.delete()    

        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address


        cleaned_string = address.replace('[', '').replace(']', '')


        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]
        str1 = str()
        k = 1
        for i in cleaned_data:
            if k == 1:
                str1+=i
            else:
                str1+=" "+i
            k = 2

        str1 = str1.replace(","," ")
                

        draft_order.shipping_address = str1
        draft_order.save()


        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':draft_order.order_grandtotal,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    }
    return render(request,'userside/user_orders/order-success.html',context)




@login_required
def get_invoice(request,id):

    user_id = request.user.id
    user = User.objects.get(id = user_id)
    order_actual_total = 0
    order = Order.objects.get(id = id)
    order_products = OrderProduct.objects.filter(order = order)

    for i in order_products:
        order_actual_total += i.product_price

    context = {
        "user" : user,
        "order" : order,
        "order_products" : order_products,
        "order_actual_total":order_actual_total,
    }


    return render(request,"userside/user_orders/order_invoice.html",context)
