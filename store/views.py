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
from offer_management.models import ReferralOffer,ReferralUser

def store(request, category_slug=None):
    products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True)
    
    products_list = []

    for product in products:
        variants = Product_Variant.objects.filter(is_active=True, product=product.id)
        for variant in variants:
            products_list.append(variant)

    if request.method == "POST":
        selected_categories = request.POST.getlist('category')

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
    paged_products = paginator.get_page(page)
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

    
    product_variant = Product_Variant.objects.get(id=id)
    p_id = product_variant.product_id
    product_variant_select = Product_Variant.objects.filter(product_id=p_id)
    for i in product_variant_select:
        i.apply_category_offer_discount()

    

    product = Product.objects.filter(is_available=True,id=id)
    product_all = Product.objects.filter(is_available=True)
    product_variants_list = []
    product_variant_all = Product_Variant.objects.filter(is_active=True)
    
    products_list = list()
    for pro in product_all:
        variants = Product_Variant.objects.filter(is_active=True,product=pro.id)
        for variant in variants:
            product_variants_list.append(variant)
            break
    product_images = Additional_Product_Image.objects.filter(product_variant = id)

    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product_variant).exists()

    product_context = {
        'product_variant':product_variant,
        'product_variants_list':product_variants_list,
        'product_images':product_images,
        'product_variant_select':product_variant_select,
        'in_cart':in_cart
    }
    
    return render(request,'userside/shopdetails.html',product_context)


@never_cache
def userside_search(request):

    if request.method == 'POST':
        product = request.POST["search_product"]
        if product != '':
            products_list = Product_Variant.objects.filter(variant_name__istartswith=product, is_active=True, product__brand__is_active=True, product__brand__isnull=False, product__category__is_active=True)  # Filter out products with no brand and inactive brands
    
                

            categories_with_product_variants = Category.objects.annotate(
            num_product_variants=models.Count('product__products')
            ).filter(num_product_variants__gt=0, is_active=True)
            context = {
                'products_list': products_list,
                'categories':categories_with_product_variants,
            }
            return render(request, 'userside/store.html', context)
        else:
            # If the search product is empty, redirect to the store
            return redirect('store_app:products_by_category')
    else:
        # Handle GET requests, if any
        return redirect('store_app:products_by_category')  # Redirect to the store in case of GET requests
    

@never_cache
def user_category_search(request,id):
    category = Category.objects.get(id=id)
    products_list = Product_Variant.objects.filter(product__category=category, is_active=True)
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    

    context = {
        'products_list': paged_products
    }
    return render(request, 'userside/store.html', context)


def low_to_high(request):

    if request.method == "POST":
        print("TTTTTTTTTTTTTTTTTTTTTTT")
        selected_categories = request.POST.getlist('category')

        # Filter products based on selected categories
        if selected_categories:
            filtered_products = []
            for category_id in selected_categories:
                category_products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True, category__id=category_id)
                for product in category_products:
                    variants = Product_Variant.objects.filter(is_active=True, product=product.id)
                    filtered_products.extend(variants)

            # Only add unique variants to products_list
            categories_with_product_variants = Category.objects.annotate(
            num_product_variants=models.Count('product__products')
            ).filter(num_product_variants__gt=0, is_active=True)
            products_list = list(set(filtered_products))
            paginator = Paginator(products_list,6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)    

            context = {
                'products_list': paged_products,
                'categories':categories_with_product_variants
            }
            return render(request, 'userside/store.html', context)
    
    products_list = Product_Variant.objects.filter(is_active=True).order_by('sale_price')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)

    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    

    context = {
        'products_list': paged_products,
        'categories':categories_with_product_variants
    }
    return render(request, 'userside/store.html', context)



def high_to_low(request):


    if request.method == "POST":
            print("TTTTTTTTTTTTTTTTTTTTTTT")
            selected_categories = request.POST.getlist('category')

            # Filter products based on selected categories
            if selected_categories:
                filtered_products = []
                for category_id in selected_categories:
                    category_products = Product.objects.filter(category__is_active=True, is_available=True, brand__is_active=True, category__id=category_id)
                    for product in category_products:
                        variants = Product_Variant.objects.filter(is_active=True, product=product.id)
                        filtered_products.extend(variants)

                # Only add unique variants to products_list
                categories_with_product_variants = Category.objects.annotate(
                num_product_variants=models.Count('product__products')
                ).filter(num_product_variants__gt=0, is_active=True)
                products_list = list(set(filtered_products))
                paginator = Paginator(products_list,6)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)    

                context = {
                    'products_list': paged_products,
                    'categories':categories_with_product_variants
                }
                return render(request, 'userside/store.html', context)
        
    products_list = Product_Variant.objects.filter(is_active=True).order_by('-sale_price')
    categories_with_product_variants = Category.objects.annotate(
    num_product_variants=models.Count('product__products')
    ).filter(num_product_variants__gt=0, is_active=True)
    
    paginator = Paginator(products_list,6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)    

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

    cart_items = CartItem.objects.filter(user = request.user)
    list1 = list()
    for i in cart_items:
        list1.append(i.product.id)

    wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist)
    print("wishlist_items before", wishlist_items)
    for i in wishlist_items:
        if i.product.id in list1:
            i.delete()
    print("wishlist items after",wishlist_items)

    context = {
       'wishlist_items':wishlist_items ,
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


def referral(request):
    user = request.user
    user_referral = ReferralUser.objects.get(user = user)
    context = {
        'user_referral':user_referral,
    } 
    return render(request,'userside/referral.html',context)



