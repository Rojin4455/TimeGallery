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

    path('add_product_variant/<int:id>/',views.add_product_variant, name='add-product-variant'),
    path('product-variant-list/<int:id>/',views.product_variant_list, name='product-variant-list'),
    # path('add-variant-attribute/',views.add_variant_attribute, name='add-variant-attribute'),
    path('attribute-values/',views.attribute_values, name='attribute-values'),
    # path('block-attribute-value/<int:attribute_value_id>/', views.block_attribute_value, name='block_attribute_value'),

    path('deactivate_attribute/<int:id>/', views.deactivate_attribute, name='deactivate_attribute'),
    path('activate_attribute/<int:id>/', views.activate_attribute, name='activate_attribute'),


    path('edit-product-variant/<int:id>/', views.edit_product_variant, name='edit-product-variant'),
    path('delete-product-variant/<int:id>/', views.delete_product_variant, name='delete-product-variant'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('coupon_list/', views.coupon_list, name='coupon_list'),
    path('toggle_coupon_status/', views.toggle_coupon_status, name='toggle_coupon_status'),















]