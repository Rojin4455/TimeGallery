from django.shortcuts import render

# Create your views here.
def admin_login(request):
    return render(request,'admin_side/page-account-login.html')

def admin_dashboard(request):
    return render(request,'admin_side/page-admin-dashboard.html')

def admin_products_list(request):
    return render(request,'admin_side/page-products-list.html')

def admin_orders(request):
    return render(request,'admin_side/page-orders-1.html')

def admin_catagories(request):
    return render(request,'admin_side/page-categories.html')

def admin_add_products(request):
    return render(request,'admin_side/page-form-product-3.html')

def admin_users_list(request):
    return render(request,'admin_side/page-users-list.html')

def admin_logout(request):
    return render(request,'admin_side/page-account-login.html')

# def admin_dashboard(request):
#     return render(request,'admin_side/base.html')
