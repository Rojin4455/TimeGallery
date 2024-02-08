from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug': ('cat_name',)}
    list_display = ('cat_name', 'cat_slug')

admin.site.register(Category,CategoryAdmin)