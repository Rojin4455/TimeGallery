from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Product_Variant
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
import json
from django.http import JsonResponse
from store.models import Coupon,UserCoupon
from django.core.cache import cache
from django.utils import timezone
from decimal import Decimal
from django.views.decorators.http import require_POST







# Create your views here.

#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    print("already exit cart id: ",cart)
    if not cart:
        cart = request.session.create()
        print("created cart Id: ",cart)
    return cart


def add_cart(request, product_id):
    product = Product_Variant.objects.get(id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        
        try:
            cart_item = CartItem.objects.get(product=product , user=current_user)
            cart_item.quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                cart=cart,
                quantity = 1,
            )
            print("YRERW")
            cart_item.save()
        return redirect(reverse('store_app:product_details', kwargs={'id': product.id}))
    else:

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

            # print("DIUHFIUEBWFJEBWF")
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product , cart=cart)
            cart_item.quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = 1,
            )
            print("user not authenticated")
            cart_item.save()

        return redirect(reverse('store_app:product_details', kwargs={'id': product.id}))

    

def cart(request, total=0, quantity=0, cart_items=None):

    # if request.method == "POST":
    #     # Extract coupon code from POST data
    #     coupon_code = request.POST.get("coupencode")
        
    #     # Check if coupon code is provided
    #     if coupon_code:
    #         try:
    #             # Get the coupon object
    #             coupon = Coupon.objects.get(coupon_code=coupon_code, is_expired=False)
                
    #             # Apply coupon discount to cart items
    #             if request.user.is_authenticated:
    #                 cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    #             else:
    #                 cart = Cart.objects.get(cart_id=_cart_id(request))
    #                 cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #             total = 0
    #             for cart_item in cart_items:
    #                 # Apply discount to each cart item
    #                 # discount_amount = (coupon.discount_percentage / 100) * (int(cart_item.product.max_price) * int(cart_item.quantity))
    #                 # cart_item.subtotal -= discount_amount
    #                 # cart_item.save()
    #                 total += cart_item.subtotal()
    #             print(total)
    #             print(coupon.discount_percentage)
    #             discount_amount = int(total) * (coupon.discount_percentage / 100)
    #             total = int(total)-discount_amount
    #             request.session["total"] = total
    #             request.session["coupon_discount_amount"] = discount_amount

    #             print("fwfwf",total)

    #             return redirect('cart_app:cart')
                
    #         except Coupon.DoesNotExist:
    #             # Coupon does not exist or is expired
    #             return JsonResponse({'success': False, 'message': 'Invalid coupon code'})
        
    total_with_original_price = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
                    total += cart_item.subtotal()
                    total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
                    quantity += cart_item.quantity


        coupens = Coupon.objects.filter(is_expired=False)
        discount = total_with_original_price - total

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'discount': discount,
            'total_with_original_price': total_with_original_price,
            'coupens': coupens
        }

        return render(request, 'userside/cart.html', context)
    else:
        try:                
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                    total += cart_item.subtotal()
                    total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
                    quantity += cart_item.quantity


            coupens = Coupon.objects.filter(is_expired=False)
            discount = total_with_original_price - total

            context = {
                'total': total,
                'quantity': quantity,
                'cart_items': cart_items,
                'discount': discount,
                'total_with_original_price': total_with_original_price,
                'coupens': coupens
            }

            return render(request, 'userside/cart.html', context)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        return render(request, 'userside/cart.html')



def cart_test(request):
    return render(request,'userside/cart-test.html')

def remove_cart(request,product_id):
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
    
    return redirect('cart_app:cart')


def update_cart(request,product_id):

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

        return redirect('cart_app:cart')
    else:
        messages.error(request,'Stock Limit Exceeded')
        return redirect('cart_app:cart')


def remove_cart_item(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)
    current_user = request.user
    if current_user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=current_user)

    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart_app:cart')


def wishlist(request):
    return render(request,'userside/wishlist.html')



# @require_POST
# def apply_coupon(request):

    
    # discount_amount = 0 
    # if 'discount' in request.session:
    #     del request.session['discount']
    #     print(discount_amount,'ddiscount')

    # if discount_amount == 0 :
    #     print("DDDDDDDDDDDDDDDDDD")
    #     data = json.loads(request.body)
    #     coupon_code = data.get('coupencode')
    #     coupn_dict = {'coupon':coupon_code,}
    #     cache.set('coupon_code',coupn_dict )
    #     print(coupon_code)
    #     # grand_total = float(request.session.get('grandtotal'))
    #     # print('grandd',grand_total)
    
    #     try:
    #         # Attempt to get the Coupon object based on the provided coupon code
    #         coupon = Coupon.objects.get(coupon_code=coupon_code)
    #         print(coupon,'1')
    #     except Coupon.DoesNotExist:
    #         # Handle the case where the coupon does not exist
    #         data = {'error': 'Coupon does not exist'}
    #         return JsonResponse(data, status=200)
        
    #     try:
    #         # Attempt to get the UserCoupon object for the current user and coupon
    #         cart_item_instance= CartItem.objects.filter(user=request.user)
    #         for i in cart_item_instance:
    #             i.cart.id
    #         total = 0
    #         print(cart_item_instance)
    #         for cart_item in cart_item_instance:
    #             total += cart_item.subtotal()
    #         print("total121:   ",int(total))
    #         total = int(total)
    #         cart_instance = Cart.objects.get(id=i.cart.id)   
    #         coupon_usage, created = UserCoupon.objects.get_or_create(
    #         coupon=coupon,
    #         user=request.user,
    #         defaults={'usage_count': 0}  # Set default values for newly created instance
    #         )
    #         print(coupon_usage.usage_count)

    #         cart_instance.coupon = coupon_usage
    #         cart_instance.save()
    #         print('sucess',cart_instance)
    #         print(coupon_usage.id, '2')
    #     except UserCoupon.DoesNotExist:
    #         # Handle the case where the UserCoupon does not exist
    #         data = {'error': 'UserCoupon does not exist'}
    #         return JsonResponse(data, status=200)
        
    #     discount=coupon.discount_percentage
    #     print("discount",discount)
    #     if coupon_usage.apply_coupon() and total >= float(coupon.minimum_amount):

    #         print("FDFEWQFDWEF")
    #         print("discount",discount)
    #         print("total",total)
    #         discount_amount = (discount / 100) * total
    #         print("discount amount",discount_amount)
    #         coupon.total_coupons -= 1
    #         coupon.save()
    #         print(discount_amount, 'Success')
    #         request.session['discount'] = round(discount,2) 
    #         print('grandd',total)
    #         data={'discount_amount':discount_amount,'discount':discount}
    #         print(data,'3')
    #         return JsonResponse({'success':'Coupon Applied'})
            
    #     else:

    #         if coupon.expire_date < timezone.now().date():
    #             data={'error':'Coupon expired'}
    #             print('Failed')
    #             return JsonResponse(data)
    #         elif total < float(coupon.minimum_amount):
    #             data={'error':'Minimum amount required'}
    #             print('Failed')
    #             return JsonResponse(data)
    #         elif coupon.total_coupons == 0:
    #             data={'error':'Coupon not available'}
    #             print('Failed')
    #             return JsonResponse(data)
    #         data={'error':'Maximum uses of the coupon reached'}
    #         print('Failed')
    #         return JsonResponse(data)
        
    # else:
    # return JsonResponse({'error': 'Coupon already applied'})


