from django.shortcuts import render
from orders.models import OrderProduct
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from orders.models import Order,OrderProduct
from admin_app.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from user_app.models import Address
from admin_app.decorators import admin_login_required
from wallet.models import Wallet,WalletTransaction




@admin_login_required
def order_list(request):
    order_list = OrderProduct.objects.all().order_by("-created_at")
    order = Order.objects.all().order_by("-created_at")

    paginator = Paginator(order, 6)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)


    context = {
        "paged_orders":paged_orders,
        'order':order,
    }
    return render(request,'admin_side/orders/order_list.html', context)

@admin_login_required
def order_details(request,user_id):

    user = User.objects.get(id = user_id)

    orders = OrderProduct.objects.filter(user__id = user.id).order_by("-created_at")
    order_products_calc = OrderProduct.objects.filter(user__id = user.id,order_status__in=["New","Accepted","Delivered"],order__payment__payment_status__in=["SUCCESS","PENDING"]).order_by("-created_at")
    order = Order.objects.filter(user_id = user.id)
    total_user_orders = Order.objects.filter(user=user_id)


    
    try:
        user_address = Address.objects.get(is_default = True, account = user)
    except:
        user_address = None
    total_product_price = 0
    grant_total = 0
    discount = 0
    for i in order_products_calc:
        total_product_price += i.product_price
        grant_total += i.grand_totol

    discount = grant_total-total_product_price


    context = {
        "orders":orders,
        "order":order,
        "user_address":user_address,
        "user":user,
        "discount":discount,
        "grant_total":grant_total,
        "total_product_price":total_product_price
    }


    return render(request,'admin_side/orders/order_details.html',context)

@admin_login_required
def change_order_status(request, order_id, status, user_id):
    order_product = get_object_or_404(OrderProduct, id=order_id)

    order_product.order_status = status
    order_product.save()
    if status == "Cancelled Admin":
        order = Order.objects.get(order_number = order_product.order)


        if order.payment.is_paid:
            wallet = Wallet.objects.get(user = order.user)
            wallet.balance += order_product.grand_totol
            wallet.save()
            WalletTransaction.objects.create(
                wallet = wallet,
                transaction_type = "CREDIT",
                transaction_detail = 'Order product Cancelled by Admin',
                amount = order_product.grand_totol
            )

    elif status == "Delivered":
        order = Order.objects.get(order_number = order_product.order)
        if order.payment.payment_method.method_name == "CASH ON DELIVERY":
            order_product.is_paid = True
            order_product.save()
            order.payment.amount_paid = order_product.grand_totol
            order.save()
            
    
    # Redirect to some page after changing status
    return redirect(reverse('order_management_app:order_details', kwargs={'user_id': user_id}))


@admin_login_required
def order_list_details(request,id):
    order = Order.objects.get(id = id)
    order_products = OrderProduct.objects.filter(order = order)
    user_id = order.user.id
    user = User.objects.get(id = user_id)

    try:
        user_address = Address.objects.get(is_default = True, account = user)
    except:
        user_address = None
    total_product_price = 0
    grant_total = 0
    discount = 0
    for i in order_products:
        total_product_price += i.grand_totol
    if total_product_price > order.order_total:
        order_total =  order.order_total
        coupon_discount = total_product_price-order_total
    shipping_address = order.shipping_address
    try:
        context={
            'order':order,
            'order_products':order_products,
            'user':user,
            'shipping_address':shipping_address,
            'coupon_discount':coupon_discount,
            'order_total':order_total,
            'total_product_price':total_product_price
        }
    except:
        context={
            'order':order,
            'order_products':order_products,
            'user':user,
            'shipping_address':shipping_address,
            'total_product_price':total_product_price
        }


    return render(request,'admin_side/orders/order_list_details.html',context)

