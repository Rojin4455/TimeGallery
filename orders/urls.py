from django.urls import path, include
from . import views

app_name = 'order_app'
urlpatterns = [
    path('place_order_cod/', views.place_order_cod, name='place_order_cod'),
    path('profile-order-details/<int:id>/', views.profile_order_details, name='profile_order_details'),
    path('cancel-product/<int:item_id>/', views.cancel_product, name='cancel_product'),
    path('return-product/<int:item_id>/', views.return_product, name='return_product'),
    path('place_order_razpay/', views.place_order_razpay, name='place_order_razpay'),
    path('order_success/<razorpay_order_id>/<payment_id>/<signature>/', views.order_success, name='order_success'),
    path('paymentfail/', views.paymentfail, name='paymentfail'),




]
