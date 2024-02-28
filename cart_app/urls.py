from django.urls import path
from .import views
app_name = 'cart_app'


urlpatterns = [
    path('cart/',views.cart, name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    # path('cart-test/',views.cart_test,name='cart_test'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('update_cart/<int:product_id>/',views.update_cart,name='update_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),





]


