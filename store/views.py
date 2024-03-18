from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,Brand,Product_Variant
from category.models import Category
from django.contrib import messages
from . models import Additional_Product_Image
from django.views.decorators.cache import never_cache
from cart_app.views import CartItem,_cart_id,Cart
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db import models
from .models import Wishlist,WishlistItem
from admin_app.models import User

def store(request, category_slug=None):
    # Assuming this is the initial retrieval of products without category filter
    products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True)
    
    # List to store product variants
    products_list = []

    # Fetch product variants for each product
    for product in products:
        variants = Product_Variant.objects.filter(is_active=True, product=product.id)
        for variant in variants:
            products_list.append(variant)

    # Handle form submission
    if request.method == "POST":
        selected_categories = request.POST.getlist('category')  # Get list of selected categories

        # Filter products based on selected categories
        if selected_categories:
            filtered_products = []
            for category_id in selected_categories:
                category_products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True, category__id=category_id)
                for product in category_products:
                    variants = Product_Variant.objects.filter(is_active=True, product=product.id)
                    filtered_products.extend(variants)

            # Only add unique variants to products_list
            products_list = list(set(filtered_products))

    # Pagination
    paginator = Paginator(products_list, 6)
    page = request.GET.get('page')
    print("page no:    ",page)
    paged_products = paginator.get_page(page)
    print(type(paged_products))
    # Get all categories with at least one product variant associated
    categories_with_product_variants = Category.objects.annotate(
        num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)

    context = {
        'products_list': paged_products,
        'categories': categories_with_product_variants
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
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    


    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': paged_products
    }
    return render(request, 'userside/store.html', context)


def low_to_high(request):
    products_list = Product_Variant.objects.filter(is_active=True).order_by('sale_price')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)

    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    


    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': paged_products,
        'categories':categories_with_product_variants
    }
    return render(request, 'userside/store.html', context)



def high_to_low(request):
    products_list = Product_Variant.objects.filter(is_active=True).order_by('-sale_price')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)
    
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    


    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': paged_products,
        'categories':categories_with_product_variants
    }
    return render(request, 'userside/store.html', context)


def aA_to_zZ(request):
    
    products_list = Product_Variant.objects.filter(is_active=True).order_by('variant_name')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)
    
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    


    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': paged_products,
        'categories':categories_with_product_variants
    }
    return render(request, 'userside/store.html', context)


def Zz_to_Aa(request):

    products_list = Product_Variant.objects.filter(is_active=True).order_by('-variant_name')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)
    
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    


    # products = Product.objects.filter(is_available=True,brand__is_active=True, category__is_active=True,category=id)
    # product_variants = Product_Variant.objects.filter(product=products)
    # # products = Product.objects.filter(is_available=True, brand__is_active=True, brand__isnull=False, category__is_active=True, category=id)  # Filter out products with no brand and inactive brands
    # products_list = product_variants
    context = {
        'products_list': paged_products,
        'categories':categories_with_product_variants
    }
    return render(request, 'userside/store.html', context)


def pricebar(request):
    return render(request,'userside/pricebar_sample.html')


def wishlist(request):
    user_id = request.user.id

    user = User.objects.get(id = user_id)
    try:
        user_wishlist = Wishlist.objects.get(user=user)
    except:
        user_wishlist = Wishlist.objects.create(user=user)

    wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist)
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # cart_items = CartItem.objects.filter(cart=cart, is_active=True,user=user)
    # for i in cart_items:
    #     print(i)
    
    context = {
       'wishlist_items':wishlist_items ,
    #    'cart_items':cart_items
    }
    return render(request,'userside/wishlist.html',context)


def add_wishlist(request,id):
    user_id = request.user.id

    user = User.objects.get(id = user_id)
    product_variant = Product_Variant.objects.get(id=id)
    try:
        user_wishlist = Wishlist.objects.get(user=user)
    except:
        user_wishlist = Wishlist.objects.create(user=user)

    wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist,product = product_variant)
    if not wishlist_items:
       WishlistItem.objects.create(wishlist=user_wishlist,product = product_variant)
    else:
        messages.error(request,'item is already in your wishlist')
        id = product_variant.id
        return redirect('store_app:product_details',id)
    return redirect('store_app:wishlist')


def wishlist_remove(request,id):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    product_variant = Product_Variant.objects.get(id=id)
    user_wishlist = Wishlist.objects.get(user=user)
    wishlist_items = WishlistItem.objects.get(wishlist=user_wishlist,product = product_variant)
    wishlist_items.delete()
    return redirect('store_app:wishlist')



