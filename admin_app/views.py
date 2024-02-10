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


# def admin_products_list(request):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     brands = Brand.objects.all()
#     context = {
#         'products':products,
#         'categories':categories,
#         'brands':brands,
#     }
#     return render(request,'admin_side/page-products-list.html',context)

def admin_orders(request):
    return render(request,'admin_side/page-orders-1.html')

# def admin_catagories(request):
#     return render(request,'admin_side/page-categories.html')

# def admin_add_products(request):
#     return render(request,'admin_side/page-form-product-3.html')

# def admin_users_list(request):
#     return render(request,'admin_side/page-users-list.html')

# def admin_logout(request):
#     return render(request,'admin_side/page-account-login.html')

# def admin_dashboard(request):
#     return render(request,'admin_side/base.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @never_cache
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

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def admin_logout(request):
    logout(request)
    return redirect('admin_app:admin_login')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @never_cache
def admin_dashboard(request):
    
    if request.user.is_superuser:
        if request.user.is_authenticated:
            return render(request,'admin_side/page-admin-dashboard.html')
        return redirect('admin_app:admin_login')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def user_list(request):
#     if request.user.is_superuser:
#         if request.user.is_authenticated:
#             user = User.objects.all()
#             user_all = {
#                 'user':user
#             }
#             return render(request,'admin_side/page-users-list.html',user_all)
#         return redirect('admin_app:admin_login')

        

# def edit_category(request):

#     return render(request,'admin_side/edit-category.html')