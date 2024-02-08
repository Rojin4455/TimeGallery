
from django.urls import path
from .import views

app_name = 'store_app'

urlpatterns = [
    path('store/',views.store, name='store'),
    # path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('products_by_category',views.store, name='products_by_category'),



]


