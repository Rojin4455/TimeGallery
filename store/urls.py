
from django.urls import path
from .import views

app_name = 'store_app'

urlpatterns = [
    # path('store/',views.store, name='store'),
    # path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('products-by-category/',views.store, name='products_by_category'),
    path('product-details/<int:id>/',views.product_details, name='product_details'),
    path('userside_search/',views.userside_search, name='userside_search'),
    # path('add-variant-attribute/',views.add_variant_attribute, name='add-variant-attribute'),
    path('user-category-search/<int:id>/',views.user_category_search, name='user_category_search'),
    path('low_to_high/',views.low_to_high, name='low_to_high'),
    path('high_to_low/',views.high_to_low, name='high_to_low'),
    path('aA_to_zZ/',views.aA_to_zZ, name='aA_to_zZ'),
    path('Zz_to_Aa/',views.Zz_to_Aa, name='Zz_to_Aa'),






]


