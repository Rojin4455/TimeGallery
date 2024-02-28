from django.urls import path
from . import views

app_name = 'checkout_app'
urlpatterns = [
    path('checkout/',views.checkout_address,name='checkout_address'),
    path('checkout_edit_address/<int:id>/',views.checkout_edit_address,name='checkout_edit_address'),
    path('checkout_create_address/',views.checkout_create_address,name='checkout_create_address'),
    path('order_summary/',views.order_summary,name='order_summary'),
    path('checkout-payment/',views.checkout_payment,name='checkout_payment'),
    path('order-success/',views.order_success,name='order_success'),



]