from django.urls import path
from . import views

app_name = 'product_management_app'

urlpatterns = [
    path('admin-products-list',views.admin_products_list,name='admin_products_list'),
    path('add-product/',views.add_product, name='add_product'),
    path('add_extra_images/',views.add_extra_images, name='add_extra_images'),
    path('deactivate_brand/<int:id>',views.deactivate_brand, name='deactivate_brand'),
    path('activate_brand/<int:id>',views.activate_brand, name='activate_brand'),
    path('edit-product/<int:id>',views.edit_product, name='edit_product'),
    path('deactivate_product/<int:id>',views.deactivate_product, name='deactivate_product'),
    path('activate_product/<int:id>',views.activate_product, name='activate_product'),


    path('show_actived_products/',views.show_actived_products, name='show_actived_products'),
    path('show_inactive_products/',views.show_inactive_products, name='show_inactive_products'),
    # path('show_all_products/',views.show_all_products, name='show_all_products'),

    # path('search_product/<int:id>',views.search_product, name='search_product'),







]