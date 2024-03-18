from django.db import models
from category.models import Category
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q, F, Avg, Count
from django.urls import reverse
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from admin_app.models import User
from django.db import models
from django.utils import timezone
from django.utils import timezone
from decimal import Decimal




class Brand(models.Model):
    brand_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    images = models.ImageField(upload_to='photos/products', null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.slug:
            product_slug_name = f'{self.brand.brand_name}-{self.product_name}-{self.category.cat_name}'
            base_slug = slugify(product_slug_name)
            counter = Product.objects.filter(slug__startswith=base_slug).count()
            if counter > 0:
                self.slug = f'{base_slug}-{counter}'
            else:
                self.slug = base_slug
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand.brand_name + "-" + self.product_name


class Attribute_Value(models.Model):
    attribute_value = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.attribute_value)
        super(Attribute_Value, self).save(*args, **kwargs)

    def __str__(self):
        return self.attribute_value

class Product_Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    variant_name = models.CharField(max_length=150, null=True)
    sku_id = models.CharField(max_length=30, blank=True)
    attributes = models.ManyToManyField(Attribute_Value, related_name='attributes')
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True, blank=True, max_length=200)
    thumbnail_image = models.ImageField(upload_to='media/photos/product_variant/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    offer = models.BooleanField(default=False,null = True)
    offer_discount =  models.DecimalField(max_digits=8, decimal_places=2,default=0, null=True)

    # k = 5
    def save(self, *args, **kwargs):
        if not self.sku_id:
            # Extracting relevant information for the SKU ID
            brand_initial = self.product.brand.brand_name[:3].upper()
            product_id = self.product.id
            # Check if attributes exist before accessing
            # color = self.attributes.first().attribute_value if self.attributes.exists() else 'NOCOLOR'
            # Generating SKU ID in the specified format
            self.sku_id = f'{brand_initial}-{product_id}'

        # Generate and save product_variant_slug
        product_variant_slug_name = f'{self.product.brand.brand_name}-{self.product.product_name}-{self.product.category.cat_name}-{self.sku_id}'
        base_slug = slugify(product_variant_slug_name)
        counter = Product_Variant.objects.filter(product=self.product).count()
        # if counter > 0:
        
        self.product_variant_slug = f'{base_slug}-{str(counter)+str(self.pk)}'
        # Product_Variant.k += 1
        # else:
        #     self.product_variant_slug = base_slug

        super(Product_Variant, self).save(*args, **kwargs)

        # Resize the thumbnail image before saving
        if self.thumbnail_image:
            img = Image.open(self.thumbnail_image.path)
            desired_size = (522, 522)

            # Create a new blank image with the desired size
            new_img = Image.new("RGB", desired_size, (255, 255, 255))
            # Paste the original image onto the new image, centered and with cropping
            img = ImageOps.fit(img, desired_size, Image.LANCZOS)  # Use Image.LANCZOS for high-quality downsampling

            # Paste the fitted image onto the new blank image
            x_offset = (desired_size[0] - img.size[0]) // 2
            y_offset = (desired_size[1] - img.size[1]) // 2
            new_img.paste(img, (x_offset, y_offset))

            # Save the new image
            new_img.save(self.thumbnail_image.path)

            print(f"Image saved: {self.thumbnail_image.path}")  # Add this line for debugging




    def apply_category_offer_discount(self):
        from offer_management.models import CategoryOffer
        from category.models import Category

        category = self.product.category
        category_offer = CategoryOffer.objects.filter(category=category, is_active=True).order_by('-id').first()
        
        if category_offer:
            print("Category offer triggered:", category_offer.discount_percentage)
            discount_decimal = Decimal(category_offer.discount_percentage) / 100
            print("Discount decimal:", discount_decimal)
            
            try:
                # Convert sale_price to Decimal
                sale_price_decimal = Decimal(str(self.sale_price))
                discount_amount = sale_price_decimal * discount_decimal
                print("Discount amount:", discount_amount)
            except Exception as e:
                print("Exception while calculating discount amount:", e)
                return 0
            
            # Apply the discount
            self.sale_price = str(sale_price_decimal - discount_amount)  # Convert back to str
            self.offer = True
            self.offer_discount = discount_amount
            self.save()
            print("Discount amount applied:", discount_amount)
            return discount_amount
        else:
            print("No category offer found")
            return 0



            
    def get_product_name(self):
        return f'{self.product.product_brand} {self.product.product_name} - {", ".join([value[0] for value in self.atributes.all().values_list("atribute_value")])}'    

    def __str__(self):
        return self.product_variant_slug

    def get_product_name(self):
        return f'{self.product.product_name}'    


    def __str__(self):
        # return self.thumbnail_image.url
        return self.variant_name


# class  Additional_Product_Image(models.Model):
#     product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_product_images')
#     image       = models.ImageField(upload_to='photos/product_additional')
#     is_active   = models.BooleanField(default=True)

#     def __str__(self):
#         return self.image.url
    
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE, related_name='additional_product_images')
    image = models.ImageField(upload_to='media/photos/additional_photos')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure proper saving
        super().save(*args, **kwargs)

        # Open the uploaded image using PIL
        if self.image:
            img = Image.open(self.image.path)
            desired_size = (522, 522)

            # Create a new blank image with the desired size
            new_img = Image.new("RGB", desired_size, (255, 255, 255))
            # Paste the original image onto the new image, centered and with cropping
            img = ImageOps.fit(img, desired_size, Image.LANCZOS)  # Use Image.LANCZOS for high-quality downsampling

            # Paste the fitted image onto the new blank image
            x_offset = (desired_size[0] - img.size[0]) // 2
            y_offset = (desired_size[1] - img.size[1]) // 2
            new_img.paste(img, (x_offset, y_offset))

            # Save the new image
            new_img.save(self.image.path)

            print(f"Image saved: {self.image.path}")  # Add this line for debugging

    def __str__(self):
        return self.image.url
    



    ################## COUPON ######################
# class Coupon(models.Model):
#     coupon_code         = models.CharField(max_length=100)
#     is_expired          = models.BooleanField(default=False)
#     discount_percentage = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     minimum_amount      = models.IntegerField(default=400)
#     max_uses            = models.IntegerField(default=10, validators=[MinValueValidator(0)])
#     expire_date         = models.DateField()
#     total_coupons       = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    
#     # if number of the coupon is 0 or the expired date is over set it as expired

#     def save(self, *args, **kwargs):
#         # Get the current date
#         current_date = timezone.now().date()
        
#         # Compare expire_date with current_date
#         if self.total_coupons <= 0 or self.expire_date < current_date:
#             self.is_expired = True
#         else:
#             self.is_expired = False
#         # Save the instance
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return self.coupon_code
    



class Coupon(models.Model):
    coupon_code = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=10)
    minimum_amount = models.IntegerField(default=400)
    max_uses = models.IntegerField(default=10)
    expire_date = models.DateField()
    total_coupons = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Get the current date
        current_date = timezone.now().date()
        
        # Compare expire_date with current_date
        if self.total_coupons <= 0 or self.expire_date < current_date:
            self.is_expired = True
        else:
            self.is_expired = False
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.coupon_code


class UserCoupon(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon      = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0, blank=True)

    def apply_coupon(self):
        if self.coupon.is_expired:
            print('Coupon is expired')
            return False  # Coupon i
        if self.usage_count >= self.coupon.max_uses:
            print('Maximum uses reached')
            return False
        
        # self.usage_count += 1
        # self.save()
        print('Coupon applied successfully In UserCoupon')
        return True




class Wishlist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    
    
    def __str__(self): 
        return str(self.user)
    
    def get_items_count(self):
       return self.wishlistitem_set.filter(is_active=True).count()

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE, related_name = 'wishlist')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)