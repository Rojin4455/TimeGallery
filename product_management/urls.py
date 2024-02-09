from django.urls import path
from . import views

app_name = 'product_management_app'

urlpatterns = [
    path('admin-products-list',views.admin_products_list,name='admin_products_list'),
    path('add-product/',views.add_product, name='add_product'),


]