from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,Brand,Product_Variant
from category.models import Category
from django.contrib import messages
from . models import Additional_Product_Image
from django.views.decorators.cache import never_cache
from cart_app.views import CartItem,_cart_id
from django.http import HttpResponse


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

        products_list = list()
        p = Product_Variant.objects.all()
        for pro in products:
            variants = Product_Variant.objects.filter(is_active=True,product=pro.id)
            print(pro.id)
            for variant in variants:
                products_list.append(variant)
                break
    else:
        products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True)
        products_list = list()
        p = Product_Variant.objects.all()
        for pro in products:
            variants = Product_Variant.objects.filter(is_active=True,product=pro.id)
            print(pro.id)
            for variant in variants:
                products_list.append(variant)
                break

    
    context = {
        'products_list': products_list
    }

    return render(request, 'userside/store.html', context)

def product_details(request, id):
    # print(id)
    product_variant = Product_Variant.objects.get(id=id)
    p_id = product_variant.product_id
    product_variant_select = Product_Variant.objects.filter(product_id=p_id)
    # for variant in product_variant_select:
    #     print(variant.thumbnail_image.url)
    # print(p_id)
    # product1 = Product.objects.get(id=p_id)
    # print(product1.base_price)
    # print("its the product variant product id: ", product_variant.product)
    # product = product_variant.product  # Use the product foreign key of the product_variant
    # print(product)

    product = Product.objects.filter(is_available=True,id=id)
    product_all = Product.objects.filter(is_available=True)
    product_variants_list = []
    # products_all = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active = True)  # Filter out products with no brand and inactive brands
    product_variant_all = Product_Variant.objects.filter(is_active=True)
    # product_variant_select = Product_Variant.objects.filter(is_active=True,product=id)
    
    products_list = list()
    for pro in product_all:
        variants = Product_Variant.objects.filter(is_active=True,product=pro.id)
        for variant in variants:
            product_variants_list.append(variant)
            break
    product_images = Additional_Product_Image.objects.filter(product_variant = id)
    # print("its product variant list: ",product_variants_list)

    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product_variant).exists()
    # return HttpResponse(in_cart)

    # print(product_variant_select)
    product_context = {
        'product_variant':product_variant,
        'product_variants_list':product_variants_list,
        'product_images':product_images,
        'product_variant_select':product_variant_select,
        'in_cart':in_cart
    }
    # print(product_variant_select)
    
    return render(request,'userside/shopdetails.html',product_context)


@never_cache
def userside_search(request):

    if request.method == 'POST':
        product = request.POST["search_product"]
        if product != '':
            products_list = Product_Variant.objects.filter(variant_name__istartswith=product, is_active=True, product__brand__is_active=True, product__brand__isnull=False, product__category__is_active=True)  # Filter out products with no brand and inactive brands
            context = {
                'products_list': products_list
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
    category = Category.objects.get(id=id)
    products_list = Product_Variant.objects.filter(product__category=category, is_active=True)

    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': products_list
    }
    return render(request, 'userside/store.html', context)





