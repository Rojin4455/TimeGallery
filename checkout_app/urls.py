from django.urls import path
from . import views

app_name = 'checkout_app'
urlpatterns = [
    path('checkout-address/',views.checkout_address,name='checkout_address'),
    path('checkout_edit_address/<int:id>/',views.checkout_edit_address,name='checkout_edit_address'),
    path('checkout_create_address/',views.checkout_create_address,name='checkout_create_address'),
    path('order_summary/',views.order_summary,name='order_summary'),
    path('checkout-payment-cod/',views.checkout_payment_cod,name='checkout_payment_cod'),
    # path('order-success/',views.order_success,name='order_success'),



]