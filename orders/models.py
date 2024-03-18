from django.db import models
from admin_app.models import User
import datetime




class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.method_name

class Payment(models.Model):

    PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        )
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment_method  = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_order_id = models.CharField(max_length=100,null=True,blank=True)
    amount_paid = models.CharField(max_length=30)
    payment_status =    models.CharField(choices = PAYMENT_STATUS_CHOICES,max_length=20)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_signature   = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if payment status is 'SUCCESS'
        if self.payment_status == 'SUCCESS':
            # If yes, set is_paid to True
            self.is_paid = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.payment_id)
    



class Order(models.Model):
    ORDER_STATUS_CHOICES =(
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        ("Cancelled_Admin", "Cancelled Admin"),
        ("Cancelled_User", "Cancelled User"),
        ("Returned_User", "Returned User"),
        )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment = models.OneToOneField(Payment,on_delete=models.SET_NULL,null=True,blank=True,related_name='order')
    order_number = models.CharField(max_length=100,null=True)
    shipping_address = models.TextField()
    # coupon_code = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    additional_discount = models.IntegerField(default=0,null=True)
    wallet_discount = models.IntegerField(default=0,null=True)
    order_note = models.CharField(max_length=100,blank=True,null=True)
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    order_status= models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_grandtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    
    
    def generate_order_number(self):    
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        last_order = Order.objects.filter(order_number__startswith=f'ORD{current_date}').last()
        if last_order :
            sequence_number = int(last_order.order_number[-6:]) + 1
            print(sequence_number)
            print('working')
        else:
            print('No work')
            sequence_number = 1

        return f"ORD{current_date}{sequence_number:06d}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.order_number:
            return str(self.order_number)
        else:
            return "Default Value"



class OrderProduct(models.Model):


    ORDER_STATUS_CHOICES =(
        
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        ("Cancelled_Admin", "Cancelled Admin"),
        ("Cancelled_User", "Cancelled User"),
        ("Returned_User", "Returned User"),
        ("Return_pending", "Returned pending"),

        )
    order           = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_product')
    user            = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='user')
    product_variant = models.CharField(max_length=255, null=True)
    product_id      = models.CharField(max_length=25, null=True)
    quantity        = models.IntegerField()
    product_price   = models.DecimalField(max_digits=12, decimal_places=2)
    grand_totol     = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    images          = models.ImageField(upload_to='media/order/images')
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    order_status    = models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')

    
    def save(self, *args, **kwargs):
        self.grand_totol=self.product_price*self.quantity
   
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.order)}  {self.product_variant}"
