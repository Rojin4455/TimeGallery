from django.db import models

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from category.models import Category
from django.utils import timezone
from django.core.exceptions import ValidationError
from admin_app.models import User

# Create your models here.
class CategoryOffer(models.Model):
    offer_name           = models.CharField(max_length=100)
    expire_date          = models.DateField()
    category             = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey relationship with Category
    discount_percentage  = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # category_offer_slug  = models.SlugField(max_length=200, unique=True)
    # category_offer_image = models.ImageField(upload_to='media/category_offer/',blank=True)
    is_active            = models.BooleanField(default=True)
    
    # def save(self, *args, **kwargs):
    #     # Automatically generate the slug from the offer name
    #     if not self.category_offer_slug:
    #         self.category_offer_slug = slugify(self.offer_name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_name
    
    # def calculate_discounted_price(self, product_variant):
    #     return calculate_discounted_price (product_variant, self.discount_percentage)


    # def get_absolute_url(self):
    #     return reverse('category_offer_detail', kwargs={'slug': self.category_offer_slug})


########### referal offer ############

class ReferralOffer(models.Model):
    expire_date = models.DateField()
    Amount    = models.DecimalField(max_digits=5, decimal_places=2)
    limit     = models.IntegerField()
    is_active = models.BooleanField(default=True)

        

class ReferralUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    code = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.count >= self.user.referraloffer.limit:
            self.is_active = False
        super().save(*args, **kwargs)

    def clean(self):
        if self.code < 1000 or self.code > 9999:
            raise ValidationError("Code must be a 4-digit integer.")

    def __str__(self):
        return str(self.code)