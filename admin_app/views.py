from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.decorators import login_required
from category.models import Category
from store.models import Product,Brand
from django.urls import reverse_lazy
from .decorators import admin_login_required
from orders.models import Order,OrderProduct,Payment,PaymentMethod
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import datetime
from django.http import HttpResponse


@admin_login_required
def admin_orders(request):
    return render(request,'admin_side/page-orders-1.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            return redirect('admin_app:admin_dashboard')
        return redirect('admin_app:admin_login')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = authenticate(email=email, password=password)
        if admin is not None and admin.is_superuser:
            print('admin:',admin)
            login(request,admin)
            return redirect('admin_app:admin_dashboard')
        else:
            messages.warning(request,'wrong credentials !')
            return redirect('admin_app:admin_login')
    return render(request, 'admin_side/page-account-login.html')

@admin_login_required
@never_cache
def admin_logout(request):
    logout(request)
    return redirect('admin_app:admin_login')



@admin_login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def admin_dashboard(request):

    orders = Order.objects.exclude(payment__payment_status="FAILED").order_by("-created_at")
    if request.method == 'POST':
        # Get the form data
        date = request.POST.get('date')
        payment_status = request.POST.get('payment_status')


        if date and payment_status:

            orders = Order.objects.filter(created_at__contains=date,payment__payment_status = payment_status)
            print("order_product_status",orders)

            print("YES date",date)
        elif payment_status:
            print("yes paymant status",payment_status)
            orders = Order.objects.filter(payment__payment_status = payment_status)
            print(orders)
        
        elif date:
            orders = Order.objects.filter(created_at__contains=date)




    current_year = datetime.now().year
    current_month = datetime.now().month

    total_earnings = OrderProduct.objects.filter(
    created_at__year=current_year,
    created_at__month=current_month,
    order_status='Delivered'
    ).aggregate(total_earnings=Sum('grand_totol'))

    # If there are no earnings for the month, set total_earnings to 0
    total_earnings = total_earnings['total_earnings'] if total_earnings['total_earnings'] else 0

    top_selling_products = OrderProduct.objects.filter(order_status='Delivered') \
    .values('product_variant', 'product_id') \
    .annotate(total_quantity=Coalesce(Sum('quantity'), 0)) \
    .order_by('-total_quantity')[:10]

    top_10_product = []
    top_selling_brands = []
    top_selling_categories = []
    for i in top_selling_products:
        product_variant = i['product_variant']
        product_name = product_variant[10:] if len(product_variant) > 10 else product_variant
        product = Product.objects.get(product_name__contains=product_name)
        top_10_product.append(product)
        top_selling_brands.append(product.brand) 
        top_selling_categories.append(product.category)

    top_selling_brands = list(set(top_selling_brands))
    top_selling_categories = list(set(top_selling_categories))

    top_10_product = list(set(top_10_product))
                                          
    payment = Payment.objects.distinct("payment_status")
    categories = Category.objects.filter(is_active = True)
    order_products = OrderProduct.objects.filter(order_status = "Delivered")
    products = Product.objects.all()
    categories = Category.objects.all()
    
    revenue = 0
    for i in order_products:
        revenue += i.grand_totol
    

    chart_month = []
    new_users = []
    orders_count= []
    for month in range(1, 13):
        c = 0
        user_count = 0
        order_c = 0
        for item in OrderProduct.objects.filter(order_status="Delivered"):
            if item.created_at.month == month:
                c += item.quantity
                order_c += 1

        chart_month.append(c)

        for user in User.objects.all():
            if user.joined_on.month == month:
                user_count += 1
        new_users.append(user_count)

        # Count orders with payment status "SUCCESS" for the month
        for order in Order.objects.filter(payment__payment_status="SUCCESS", created_at__month=month):
            order_c += 1

        orders_count.append(order_c)


    total_orders = len(orders)
    paginator = Paginator(orders, 6)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        "paged_orders":paged_orders,
        "revenue":revenue,
        "total_orders":total_orders,
        "total_products":len(products),
        "total_categories":len(categories),
        "chart_month":chart_month,
        "new_users":new_users,
        "orders_count":orders_count,
        'categories':categories,
        'payment':payment,
        "top_selling_products":top_10_product,
        "top_selling_brands":top_selling_brands,
        "top_selling_categories":top_selling_categories,
        "total_earnings":total_earnings,


    }

    return render(request,'admin_side/page-admin-dashboard.html',context)

