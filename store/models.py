from django.db import models
from category.models import Category
from django.utils.text import slugify

class Brand(models.Model):
    brand_name  = models.CharField(max_length=50,unique=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_name        = models.CharField(max_length=100,unique = True)
    slug                = models.SlugField(max_length = 200, unique = True)
    description         = models.TextField(max_length = 500, blank = True)
    price               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default = True)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add = True)
    modified_date       = models.DateTimeField(auto_now = True)
    brand               = models.ForeignKey(Brand,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the product name
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.product_name

# for adding additional images of the product
    
class  Additional_Product_Image(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_product_images')
    image       = models.ImageField(upload_to='photos/product_additional')
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url

