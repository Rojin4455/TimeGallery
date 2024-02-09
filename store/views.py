from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,Brand
from category.models import Category
from django.contrib import messages



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

# def add_product(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#         if request.method == 'POST':
#             title = request.POST.get('product_title')
#             stock_qty = request.POST.get('stock_qty')
#             brand_id = request.POST.get('Brand')
#             description = request.POST.get('description')
#             price = request.POST.get('price')
#             category_id = request.POST.get('category_id')

#             try:
#                 image = request.FILES.get('image')
#             except :
#                 messages.warning(request,"add product image")
#                 return redirect('store_app:add_product') 

#             try:
#                 if title == '':
#                     messages.warning(request,"Add product title")
#                     return redirect('store_app:add_product')
#                 if Product.objects.get(product_name=title):
#                     messages.warning(request,"product name is already exists")
#                     return redirect('store_app:add_product')   
#             except:
#                 pass

#             if brand_id or price or category_id or stock_qty:
#                 messages.warning(request,"All fields are required")
#                 return redirect('store_app:add_product')
            
#             product = Product(
#                 product_name = title,
#                 stock = stock_qty,
#                 brand = brand_id,
#                 category = category_id,
#                 description = description,
#                 price = price,
#                 images = image
#             )
#             product.save()
#             messages.success(request, 'Product Added.')
            

#         categories = Category.objects.filter(is_active = True)
#         brands = Brand.objects.filter(is_active = True)
#         context = {
#             'categories':categories,
#             'brands':brands
#         }
#         return render(request,'admin_side/page-form-product-3.html', context)
#     return redirect('admin_app:admin_login')

        
            # try:
            #     image = request.FILES['image']
            # except :
            #     messages.warning(request,"add category image")
            #     return redirect('category_app:add_categories')
            # try:
            #     if category == '':
            #         messages.warning(request,"Add category title")
            #         return redirect('category_app:add_categories')
            #     if Categories.objects.get(category_title=category):
            #         messages.warning(request,"category is taken")
            #         return redirect('category_app:add_categories')
            # except:
            #     pass
