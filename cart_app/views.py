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
    if not cart:
        cart = request.session.create()
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
            cart_item.save()
        return redirect(reverse('store_app:product_details', kwargs={'id': product.id}))
    else:

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

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
            cart_item.save()

        return redirect(reverse('store_app:product_details', kwargs={'id': product.id}))

    

def cart(request, total=0, quantity=0, cart_items=None):
        
    total_with_original_price = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        cart_items_first = CartItem.objects.filter(user=request.user, is_active=True).first()
        try:
            c_item = CartItem.objects.get(id = cart_items_first.id)
            cart = Cart.objects.get(cart_id=c_item.cart)
            cart.coupon_applied = None
            cart.coupon_discount = 0
            cart.save()
        except:
            pass

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


