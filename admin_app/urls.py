from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('admin-login',views.admin_login,name='admin_login'),
    path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),  
    # path('admin-products-list',views.admin_products_list,name='admin_products_list'),
    path('admin-orders',views.admin_orders,name='admin_orders'),
    # path('admin-catagories',views.admin_catagories,name='admin_catagories'),
    # path('admin-add-products',views.admin_add_products,name='admin_add_products'),
    # path('admin-users-list',views.admin_users_list,name='admin_users_list'),
    path('admin-logout',views.admin_logout,name='admin_logout'),
    # path('edit_category',views.edit_category,name='edit_category'),

]