from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Product_Variant
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages



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

    # return redirect('store_app:product_details')



def cart(request, total=0, quantity=0, cart_items=None):
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

    return render(request,'userside/cart.html', context)


def cart_test(request):
    return render(request,'userside/cart-test.html')

def remove_cart(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)
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
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)


    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_app:cart')

def remove_cart_item(request,product_id):
    product = get_object_or_404(Product_Variant,id=product_id)
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart_app:cart')



    



