from django.urls import path
from . import views

app_name = 'checkout_app'
urlpatterns = [
    path('checkout-address/',views.checkout_address,name='checkout_address'),
    path('checkout_edit_address/<int:id>/',views.checkout_edit_address,name='checkout_edit_address'),
    path('checkout_create_address/',views.checkout_create_address,name='checkout_create_address'),
    path('order_summary/',views.order_summary,name='order_summary'),


    path('remove_order_summary/<int:product_id>/',views.remove_order_summary,name='remove_order_summary'),
    path('update_order_summary/<int:product_id>/',views.update_order_summary,name='update_order_summary'),
    path('remove_order_summary_item/<int:product_id>/',views.remove_order_summary_item,name='remove_order_summary_item'),

    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('cancel_coupon/', views.cancel_coupon, name='cancel_coupon'),
]





