from django.urls import path, include
from . import views

app_name = 'order_management_app'
urlpatterns = [
    path('order-list/', views.order_list, name='order_list'),
    path('order-details/<int:user_id>', views.order_details, name='order_details'),
    path('change_status/<int:order_id>/<str:status>/<int:user_id>/', views.change_order_status, name='change_status'),



]