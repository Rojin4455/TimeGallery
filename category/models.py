from django.db import models
from django.utils.text import slugify

class Category(models.Model):

    cat_name = models.CharField(max_length=50,unique=True)
    cat_slug = models.SlugField(unique=True, max_length=200)
    cat_image = models.ImageField(upload_to='photos/cat_image',blank=True)
    cat_description = models.TextField(max_length = 255, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the product name
        if not self.cat_slug:
            self.cat_slug = slugify(self.cat_name)
        super().save(*args,**kwargs)

    def __str__(self):

        return self.cat_name



