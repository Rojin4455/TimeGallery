from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,Brand
from category.models import Category
from django.contrib import messages
from . models import Additional_Product_Image
from django.views.decorators.cache import never_cache


# from django.shortcuts import render, get_object_or_404
# from .models import Product
# from category.models import Category

from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def store(request, category_slug=None):
    products = None
    categories = None

    if category_slug is not None:
        category = get_object_or_404(Category, cat_slug=category_slug, is_active=True)
        products = Product.objects.filter(category=category, is_available=True, brand__is_active=True)
    else:
        products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active = True)  # Filter out products with no brand and inactive brands
    
    context = {
        'products': products
    }

    return render(request, 'userside/store.html', context)

def product_details(request,id):

    product = Product.objects.get(id=id)
    products_all = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active = True)  # Filter out products with no brand and inactive brands
    product_images = Additional_Product_Image.objects.filter(product = id)

    print(product_images)

    product_context = {
        'product':product,
        'products_all':products_all,
        'product_images':product_images
    }
    
    return render(request,'userside/shopdetails.html',product_context)


@never_cache
def userside_search(request):

    if request.method == 'POST':
        product = request.POST["search_product"]
        if product != '':
            products = Product.objects.filter(product_name__istartswith=product, is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True)  # Filter out products with no brand and inactive brands
            context = {
                'products': products
            }
            return render(request, 'userside/store.html', context)
        else:
            # If the search product is empty, redirect to the store
            return redirect('store_app:store')
    else:
        # Handle GET requests, if any
        return redirect('store_app:store')  # Redirect to the store in case of GET requests
    

@never_cache
def user_category_search(request,id):
    products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands

    context = {
        'products': products
    }
    return render(request, 'userside/store.html', context)



