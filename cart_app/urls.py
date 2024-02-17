from django.urls import path
from .import views
app_name = 'cart_app'


urlpatterns = [
    path('user-cart/',views.user_cart, name='user_cart'),

]


