from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity

        except Cart.DoesNotExist:
            cart_count=0
    
    return dict(cart_count=cart_count)


# myapp/context_processors.py

def global_order_summary(request):
    from .models import Cart, CartItem  # Import your Cart and CartItem models here
    from django.core.exceptions import ObjectDoesNotExist

    total = 0
    quantity = 0
    cart_items = None
    total_with_orginal_price = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.subtotal()
            total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    discount = total_with_orginal_price - total

    return {
        'global_order_summary_total': total,
        'global_order_summary_quantity': quantity,
        'global_order_summary_cart_items': cart_items,
        'global_order_summary_discount': discount,
        'global_order_summary_total_with_original_price': total_with_orginal_price,
    }
