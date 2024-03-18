from django.shortcuts import render
from orders.models import OrderProduct
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from orders.models import Order,OrderProduct
from admin_app.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from user_app.models import Address
from admin_app.decorators import admin_login_required




@admin_login_required
def order_list(request):
    order_list = OrderProduct.objects.all().order_by("-created_at")
    order = Order.objects.all().order_by("-created_at")

    paginator = Paginator(order, 6)
    page = request.GET.get('page')
    print("page no:    ",page)
    paged_orders = paginator.get_page(page)
    # print(type(paged_orders))
    # Get all categories with at least one product variant associated
    # categories_with_product_variants = Category.objects.annotate(
    #     num_product_variants=models.Count('product__products')
    # ).filter(num_product_variants__gt=0, is_active=True)

    # for i in paged_orders:
    #     print(i.)


    context = {
        "paged_orders":paged_orders,
        # "order_lists":order_list,
        'order':order,
    }
    return render(request,'admin_side/orders/order_list.html', context)

@admin_login_required
def order_details(request,user_id):

    user = User.objects.get(id = user_id)

    orders = OrderProduct.objects.filter(user__id = user.id).order_by("-created_at")
    order = Order.objects.filter(user_id = user.id)
    total_user_orders = Order.objects.filter(user=user_id)
    print("total_user_orders",total_user_orders)
    
    try:
        user_address = Address.objects.get(is_default = True, account = user)
    except:
        user_address = None
    print("user address:",user_address)
    total_product_price = 0
    grant_total = 0
    discount = 0
    for i in orders:
        total_product_price = i.product_price
        grant_total = i.grand_totol

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
    order = get_object_or_404(OrderProduct, id=order_id)
    order.order_status = status
    order.save()
    print("user_id",user_id)
    
    # Redirect to some page after changing status
    return redirect(reverse('order_management_app:order_details', kwargs={'user_id': user_id}))  # Change 'order_list' to your desired URL name


@admin_login_required
def order_list_details(request,id):
    # user = User.objects.get(id = user_id)
    order = Order.objects.get(id = id)
    order_products = OrderProduct.objects.filter(order = order)
    user_id = order.user.id
    print("user osss",user_id)
    user = User.objects.get(id = user_id)
    # address = Address.objects.get(is_default = True, account = user)
    print("userfeffefe",user.username)
    try:
        user_address = Address.objects.get(is_default = True, account = user)
    except:
        user_address = None
    print("user address:",user_address)
    total_product_price = 0
    grant_total = 0
    discount = 0
    for i in order_products:
        total_product_price += i.grand_totol
    print(total_product_price,order.order_total)
    if total_product_price > order.order_total:
        order_total =  order.order_total
        coupon_discount = total_product_price-order_total
        print("user address:",order.shipping_address)
    shipping_address = order.shipping_address
    try:
        # if coupon_discount:
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

