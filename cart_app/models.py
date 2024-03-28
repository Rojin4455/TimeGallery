from django.db import models
from store.models import Product_Variant
from user_app.models import User
from store.models import UserCoupon,Coupon

class Cart(models.Model):
    
    cart_id = models.CharField(max_length=250,blank=True)
    coupon = models.ForeignKey(UserCoupon,on_delete=models.SET_NULL,null=True)
    date_added = models.DateField(auto_now_add=True)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE, default = None,null = True)
    coupon_discount = models.IntegerField(default = 0)
    # cart_total = models.IntegerField(default = 0)
      
    def __str__(self):
        return self.cart_id
    
    def save(self, *args, **kwargs):
        if self.coupon_applied is None:
            self.coupon_discount = 0
        super(Cart, self).save(*args,**kwargs)

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def subtotal(self):
        return self.product.sale_price * self.quantity

    def __str__(self):
        return str(self.product)
    