from django.contrib import admin
from .models import Brand,Product,Coupon,UserCoupon

admin.site.register(Coupon)
admin.site.register(UserCoupon)

# Register your models here.
