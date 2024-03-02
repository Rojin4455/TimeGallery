from django.urls import path, include
from . import views

app_name = 'order_app'
urlpatterns = [
    path('place_order_cod/', views.place_order_cod, name='place_order_cod'),

]
