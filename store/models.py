from django.db import models
from category.models import Category
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F,Avg,Count
from django.urls import reverse
from PIL import Image


class Brand(models.Model):
    brand_name  = models.CharField(max_length=50,unique=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_name        = models.CharField(max_length=100,unique = True)
    slug                = models.SlugField(max_length = 200, unique = True)
    description         = models.TextField(max_length = 500, blank = True)
    # price               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products', null=True)
    # stock               = models.IntegerField()
    is_available        = models.BooleanField(default = True)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add = True)
    modified_date       = models.DateTimeField(auto_now = True)
    brand               = models.ForeignKey(Brand,on_delete=models.CASCADE)
    base_price          = models.DecimalField(max_digits=8, decimal_places=2)


    # def save(self, *args, **kwargs):
    #     # Automatically generate the slug from the product name
    #     if not self.slug:
    #         self.slug = slugify(self.product_name)
    #     super().save(*args,**kwargs)

    # def __str__(self):
    #     return self.product_name

    def save(self, *args, **kwargs):
        product_slug_name = f'{self.brand.brand_name}-{self.product_name}-{self.category.cat_name}'
        base_slug = slugify(product_slug_name)
        counter = Product.objects.filter(slug__startswith=base_slug).count()
        if counter > 0:
            self.product_slug = f'{base_slug}-{counter}'
        else:
            self.slug = base_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand.brand_name+"-"+self.product_name 

# for adding additional images of the product
    



# Atribute Table - COLOR

# class Attribute(models.Model):
#     attribute_name  = models.CharField(max_length=50,unique=True)
#     is_active       = models.BooleanField(default=True)

#     def __str__(self):
#         return self.attribute_name
    

# Atribute Value - RED,BLUE,GREEN,BLACK

class Attribute_Value(models.Model):
    attribute_value = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.attribute_value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.attribute_value



# class Product_VariantManager(models.Manager):
#     """
#     Custom manager
#     """
#     def get_all_variant(self,product):
#         # variant = super(Product_VariantManager, self).get_queryset().filter(product=product).values('sku_id','atributes__atribute_value','atributes__atribute__atribute_name')
#         variant = (
#                     super(Product_VariantManager, self)
#                     .get_queryset()
#                     .filter(product=product)
#                     .values('sku_id')
#                     # .annotate(
#                     #     atribute_value=F('atributes__atribute_value'),
#                     #     atribute_name=F('atributes__atribute__atribute_name')
#                     # )
#                 )
#         return  variant
    


class Product_Variant(models.Model):
    product              = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products')
    sku_id               = models.CharField(max_length=30,blank=True)
    attributes           = models.ManyToManyField(Attribute_Value,related_name='attributes')
    max_price            = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price           = models.DecimalField(max_digits=8, decimal_places=2)
    stock                = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True, blank=True,max_length=200)
    thumbnail_image      = models.ImageField(upload_to='media/phtots/product_variant/')
    is_active            = models.BooleanField(default=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    

    # objects = models.Manager()
    # variants = Product_VariantManager()

    def save(self, *args, **kwargs):
        if not self.sku_id:
            # Extracting relevant information for the SKU ID
            brand_initial = self.product.brand.brand_name[:3].upper()
            product_id = self.product.id
            

            # Generating SKU ID in the specified format
            self.sku_id = f'{brand_initial}-{product_id}'

        # Generate and save product_variant_slug
        product_variant_slug_name = f'{self.product.brand.brand_name}-{self.product.product_name}-{self.product.category.cat_name}-{self.sku_id}'
        base_slug = slugify(product_variant_slug_name)
        counter = Product_Variant.objects.filter(product_variant_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_variant_slug = f'{base_slug}-{counter}'
        else:
            self.product_variant_slug = base_slug

        super(Product_Variant, self).save(*args, **kwargs)

        # Resize the thumbnail image before saving
        if self.thumbnail_image:
            img = Image.open(self.thumbnail_image.path)
            size = (522,522)
            img=img.resize(size, Image.BOX)
            img.save(self.thumbnail_image.path)

    
# class  Additional_Product_Image(models.Model):
#     product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_product_images')
#     image       = models.ImageField(upload_to='photos/product_additional')
#     is_active   = models.BooleanField(default=True)

#     def __str__(self):
#         return self.image.url
    
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='additional_product_images')
    image           = models.ImageField(upload_to='media/photos/additional_photos')
    is_active       = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure proper saving
        super().save(*args, **kwargs)

        # Open the uploaded image using PIL
        if self.image:
            img = Image.open(self.image.path)
            size = (522,522)
            img=img.resize(size, Image.BOX)
            img.save(self.image.path)

    def __str__(self):
        return self.image.url

