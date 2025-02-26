from django.db import models
from admin_app.models import User

# Create your models here.

class Wallet(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username + str(self.balance)
    
class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES =(
        ("CREDIT", "CREDIT"),
        ("DEBIT", "DEBIT"),
        )
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    transaction_type= models.CharField(choices = TRANSACTION_TYPE_CHOICES,max_length=10)
    transaction_detail= models.CharField(max_length=50)
    wallet_payment_id = models.CharField(max_length=100,null=True,blank=True) #new
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_type + str(self.wallet) + str(self.amount)
