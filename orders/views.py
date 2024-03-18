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
    
    if 'discount' in request.session:
        coupon_discount = int(request.session['discount'])
        coupon_code = request.session['coupon_code']
        del request.session['discount']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 

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
    # try:
    #     if coupon_discount:
    #         discount = total_with_orginal_price - total
    #         total -= coupon_discount
    # except:
    #     discount = total_with_orginal_price - total


    # Create ShippingAddress instance
    address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]
    
    

    # Create Payment instance
    payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')
    try:

        if coupon_discount:
            discount = total_with_orginal_price - total
            total -= coupon_discount
    except:
        pass
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
    try:
        if coupon_discount:
            context = {
                            'order_dtails' : draft_order,
                            'address' : str1,
                            'order_product' : order_dtails,
                            'grand_total':total,
                            'total_with_orginal_price':total_with_orginal_price,
                            'discount':discount,
                            'coupon_discount':coupon_discount,
                            }

            return render(request,'userside/user_orders/order-success.html',context)
        # else:
        #     discount = total_with_orginal_price - total
        #     context = {
        #                 'order_dtails' : draft_order,
        #                 'address' : str1,
        #                 'order_product' : order_dtails,
        #                 'grand_total':total,
        #                 'total_with_orginal_price':total_with_orginal_price,
        #                 'discount':discount,
        #                 }
        #     return render(request,'userside/user_orders/order-success.html',context)

    except:
            discount = total_with_orginal_price - total
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

    order_products = OrderProduct.objects.filter(
    order=order).exclude(
    Q(order_status="Cancelled User") | Q(order_status="Cancelled Admin"))
    print("order productssssssssssssssssssssssssssss",order_products)
    product_total = 0
    for i in order_products:
        product_total += i.grand_totol
    print("order app order product total",product_total)
    print("order app order total ",order.order_total)
    print("product_details order",order.id)


    print("ORDer total",order.order_total)

    coupon_discount = product_total-order.order_total
    grand_total = product_total-coupon_discount
    print("coupon",coupon_discount)
    print("sdfwfefeeeeeeeeeeeeee",coupon_discount,product_total)   
    print(grand_total)
    order_products = OrderProduct.objects.filter(order=order)
    try:
        if coupon_discount > 0:
            context = {
                'order_dtails':order,
                'order_products':order_products,
                'product_total':product_total,
                'coupon_discount':coupon_discount,
                'grand_total':grand_total
            }
        else:
            context = {
                'order_dtails':order,
                'order_products':order_products,
                'grand_total':0,
            }
    except:
        pass
    return render(request,'userside/user_orders/profile-order-details.html', context)


@login_required
def cancel_product(request, item_id):
    coupon_discount_pro = 0
    ordered_product = OrderProduct.objects.get(id = item_id)
    print(ordered_product.order.id)
    order = Order.objects.get(id=ordered_product.order.id)
    order_products = OrderProduct.objects.filter(order = order)
    print("orderd productds",order_products)
    ordered_product.order_status = "Cancelled User"
    ordered_product.save()

    product_total = 0
    for product in order_products:
        product_total  += product.grand_totol
    if product_total > order.order_grandtotal:
        coupon_discount = product_total-order.order_grandtotal
        len_pro = len(order_products)
        coupon_discount_pro =coupon_discount/len_pro

    

    # payment = Order.objects.get(payment = order.payment.payment_method)
    payment_method = PaymentMethod.objects.get(method_name = order.payment.payment_method.method_name)
    print("payment method",payment_method)
    print("order number",order)

    if payment_method.method_name != "CASH ON DELIVERY":
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance+= ordered_product.grand_totol-coupon_discount_pro
        wallet.save()
        p = ordered_product.grand_totol-coupon_discount_pro
        
        order.order_total -= ordered_product.grand_totol-coupon_discount_pro
        order.save()
        WalletTransaction.objects.create(wallet = wallet,transaction_type = "CREDIT", transaction_detail = "Order Cancelled", amount = p)
        ordered_product.order_status = "Cancelled User"
        ordered_product.grand_totol = 0
        ordered_product.save()
        ordered_product_quantity = ordered_product.quantity

        product_id = ordered_product.product_id
        product_variant = Product_Variant.objects.get(id = product_id)
        product_variant.stock += ordered_product_quantity
        product_variant.save()

        # order.order_total -= p
    else:
        ordered_product_quantity = ordered_product.quantity

        product_id = ordered_product.product_id
        product_variant = Product_Variant.objects.get(id = product_id)
        product_variant.stock += ordered_product_quantity
        product_variant.save()

        order = ordered_product.order
        order_products = OrderProduct.objects.filter(order = order)
        order = Order.objects.get(id = order.id)
        ordered_product.order_status = "Cancelled User"
        order.order_total -= ordered_product.grand_totol
        ordered_product.grand_totol = 0
        ordered_product.save()
    order.save()

    
    return redirect("order_app:profile_order_details", order.id)


@login_required
def return_product(request,item_id):
    coupon_discount_pro = 0
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product.order_status = "Returned User"
    ordered_product.save()

    print(ordered_product.order.id)
    order = Order.objects.get(id=ordered_product.order.id)
    order_products = OrderProduct.objects.filter(order = order)
    
    product_total = 0
    for product in order_products:
        product_total  += product.grand_totol
    if int(product_total) > int(order.order_grandtotal):
        coupon_discount = product_total-order.order_grandtotal
        len_pro = len(order_products)
        coupon_discount_pro =coupon_discount/len_pro


    # payment = Order.objects.get(payment = order.payment.payment_method)
    payment_method = PaymentMethod.objects.get(method_name = order.payment.payment_method.method_name)

    
    if payment_method.method_name != "CASH ON DELIVERY":
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance+= ordered_product.grand_totol-coupon_discount_pro
        wallet.save()
        p = ordered_product.grand_totol-coupon_discount_pro
        
        
        WalletTransaction.objects.create(wallet = wallet,transaction_type = "CREDIT", transaction_detail = "Order Returned", amount = p)
        # ordered_product.order_status = "Returned User"
        # ordered_product.grand_totol = 0
        ordered_product.save()
        ordered_product_quantity = ordered_product.quantity

        product_id = ordered_product.product_id
        product_variant = Product_Variant.objects.get(id = product_id)
        product_variant.stock += ordered_product_quantity
        product_variant.save()
        order.order_total -= ordered_product.grand_totol-coupon_discount_pro
        print("order total after",order.order_total,ordered_product.grand_totol,coupon_discount_pro)

        # order.order_total -= p
        order.save()
    else:
        ordered_product.order_status = "Returned User"
        # ordered_product.grand_totol = 0
        ordered_product.save()
        ordered_product_quantity = ordered_product.quantity

        product_id = ordered_product.product_id
        product_variant = Product_Variant.objects.get(id = product_id)
        product_variant.stock += ordered_product_quantity
        product_variant.save()
        wallet = Wallet.objects.get(user = request.user)
        print(wallet.balance)
        wallet.balance += ordered_product.grand_totol-coupon_discount_pro
        print(wallet.balance)
        wallet.save()
        wallet_transaction = WalletTransaction.objects.create(wallet = wallet, transaction_type="CREDIT", transaction_detail="Order Returned", amount = ordered_product.grand_totol-coupon_discount_pro) 
        order = ordered_product.order
        order_products = OrderProduct.objects.filter(order = order)
        order = Order.objects.get(id = order.id)
        print("order total before",order.order_total,ordered_product.grand_totol,coupon_discount_pro)
        order.order_total -= ordered_product.grand_totol-coupon_discount_pro
        print("order total after",order.order_total,ordered_product.grand_totol,coupon_discount_pro)

        order.save()
        ordered_product.grand_totol = 0
        ordered_product.save()

        # order.order_total -= ordered_product.grand_totol

    
    print("ordered_product.grand_totol:  ",ordered_product.grand_totol)
    print("order.order_total:  ",order.order_total)

    order.save()
    print("ordered Products:  ",order_products)
    print("order :",order)
    
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




@login_required
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
    if 'discount' in request.session:
        coupon_discount = int(request.session['discount'])
        coupon_code = request.session['coupon_code']
        del request.session['discount']
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            user_coupon = UserCoupon.objects.get(user = request.user,coupon = coupon)
            user_coupon.usage_count += 1
            user_coupon.save()
        except:
            pass 
        cart_items = CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        discount = total_with_orginal_price - total
        total -= coupon_discount
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
                order_grandtotal = total
            )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        len_items = len(cart_items)
        disc_per_pro = coupon_discount/len_items
        
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
                    'coupon_discount':coupon_discount
                    }
        print('working ijgrfuhgf')
        return render(request, 'userside/user_orders/order-success.html', context)
    else:
        cart_items = CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        discount = total_with_orginal_price - total
        # total -= coupon_discount
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



def wallet_order(request):
    if 'discount' in request.session:
        coupon_discount = int(request.session['discount'])
        print("yessssssssssss",coupon_discount)
    user = request.user.id
    user_instence = User.objects.get(id = user)
    wallet = Wallet.objects.get(user = user_instence)
    amount = int(float(request.GET.get('amount', None)))
    wallet_transaction = WalletTransaction.objects.create(
            wallet = wallet,
            transaction_type = "DEBIT",
            amount = (amount-coupon_discount)
    )
    
    amount = int(float(request.GET.get('amount', None)))

    print("amount:              ",amount)


    print("wallet:",wallet)
    print("user:  ",user_instence)

    print("type of amount",type(amount))
    print("type of wallet balance:",type(wallet.balance))
    wallet.balance -= (amount-coupon_discount)
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

    if 'discount' in request.session:
        coupon_discount = int(request.session['discount'])
        coupon_code = request.session['coupon_code']
        del request.session['discount']
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
        p = total - coupon_discount


        # Create ShippingAddress instance
        address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]



        # Create Payment instance
        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=p,payment_status='SUCCESS')


        draft_order= Order.objects.create(
                user=user_instance,
                shipping_address=address1,
                order_total=total-coupon_discount,
                is_ordered  = True,
                payment = payment,
                order_grandtotal = total-coupon_discount
            )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        try:
            disc_per = coupon_discount/len(cart_items)
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
        total -= coupon_discount
        context = {
                    'order_dtails' : draft_order,
                    'address' : str1,
                    'order_product' : order_dtails,
                    'grand_total':total,
                    'total_with_orginal_price':total_with_orginal_price,
                    'discount':discount,
                    'coupon_discount':coupon_discount,
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
                # o.grand_totol -= disc_per
                # o.save()
                # print(cart_item.product.get_product_name())

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






# def cancel_product1(request,item_id):
#     item = OrderProduct.objects.get(id = id)
#     item.order_status = "Returned User"
#     item.grand_totol  = 0
#     item.save()


#     order = Order.objects.get(id = item.order.id)
#     print("order yes",order)



