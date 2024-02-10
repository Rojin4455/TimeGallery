
from django.urls import path
from .import views

app_name = 'store_app'

urlpatterns = [
    path('store/',views.store, name='store'),
    # path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('products-by-category/',views.store, name='products_by_category'),
    path('product-details/<int:id>/',views.product_details, name='product_details'),
    path('userside_search/',views.userside_search, name='userside_search'),
    path('user_category_search/<int:id>/',views.user_category_search, name='user_category_search'),





]


