"""
URL configuration for First_Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_app'
urlpatterns = [
    path('admin-default/', admin.site.urls),
    path('', include('user_app.urls')),
    path('', include('admin_app.urls')),
    path('', include('store.urls')),
    path('', include('category.urls')),
    path('', include('user_management.urls')),
    path('', include('product_management.urls')),
    path('', include('cart_app.urls')),
    path('', include('checkout_app.urls')),
    path('', include('orders.urls')),
    path('', include('order_management.urls')),
    path('', include('wallet.urls')),
    path('', include('admin_dashboard.urls')),
    path('', include('offer_management.urls')),



    path('accounts/', include('allauth.urls')),
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
