from django.shortcuts import render,get_object_or_404
from . models import Product,Category

def store(request, category_slug = None):
    products = None
    categories = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        products = Product.objects.all().filter(category = categories, is_available = True)

    else: 
        products = Product.objects.filter(is_available = True)
        context = {
        'products':products
    }

    return render(request,'userside/store.html', context)

# Create your views here.


from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request, category_slug=None):
    # products = None
    # categories = None

    # if category_slug is not None:
    #     category = get_object_or_404(Category, cat_slug=category_slug)
    #     products = Product.objects.filter(category=category, is_available=True)
    # else: 
    products = Product.objects.filter(is_available=True)

    context = {
        'products': products,
        # 'category': category  # Pass the category to the context
    }

    return render(request, 'userside/store.html', context)

