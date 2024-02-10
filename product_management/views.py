from django.shortcuts import render,redirect
from django.contrib import messages
from store.models import Product,Brand
from category.models import Category
from django.views.decorators.cache import cache_control,never_cache
from django.shortcuts import get_object_or_404
from store.models import Additional_Product_Image


@never_cache
def admin_products_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all().order_by('id')
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context = {
            'products':products,
            'categories':categories,
            'brands':brands,
        }
        return render(request,'admin_side/page-products-list.html',context)
    return redirect('admin_app:admin_login')


@never_cache
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        print("before entering post method")
        if request.method == 'POST':
            title = request.POST.get('product_title')
            stock_qty = request.POST.get('stock_qty')
            brand_id = request.POST.get('Brand')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            print("entering post method")
            image = request.FILES.get('image')
            additional_images = request.FILES.getlist('additional_image_1')


            try:
                image = request.FILES.get('image')
            except :
                messages.warning(request,"add product image")
                return redirect('product_management_app:add_product') 

            try:
                if title == '':
                    messages.warning(request,"Add product title")
                    return redirect('product_management_app:add_product')
                if Product.objects.get(product_name=title):
                    messages.warning(request,"product name is already exists")
                    return redirect('product_management_app:add_product')   
            except:
               pass
            # if brand_id or price or category_id or stock_qty:
            #     messages.warning(request,"All fields are required")
            #     return redirect('product_management_app:add_product')
            category = Category.objects.get(id = category_id)
            brand = Brand.objects.get(id = brand_id)
            product = Product(
                product_name = title,
                stock = stock_qty,
                brand = brand,
                category = category,
                description = description,
                price = price,
                images = image
            )
            product.save()
            
            for img in additional_images:
                Additional_Product_Image.objects.create(product=product,image=img)    
            

        categories = Category.objects.filter(is_active = True)
        brands = Brand.objects.filter(is_active = True)
        context = {
            'categories':categories,
            'brands':brands
        }
        return render(request,'admin_side/page-form-product-3.html', context)
    return redirect('admin_app:admin_login')



@never_cache
def edit_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=id)

        if request.method == 'POST':
            title = request.POST.get('product_title')
            stock_qty = request.POST.get('stock_qty')
            # brand_id = request.POST.get('brand')
            brand_id = request.POST.get('brand')
            brand = get_object_or_404(Brand, pk=brand_id)
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, pk=category_id)
            print("entering post method")
            image = request.FILES.get('image')
            additional_images = request.FILES.getlist('additional_image_1')
            
            if title:
                product.product_name = title
            if stock_qty:
                product.stock = stock_qty
            if brand_id:
                product.brand = brand
            if description:
                product.description = description
            if price:
                product.price = price
            if category_id:
                product.category = category
            if image:
                product.images = image
            for img in additional_images:
                Additional_Product_Image.objects.create(product=product,image=img)  

            product.save()

            return redirect('product_management_app:admin_products_list')



        brands = Brand.objects.all()
        categories = Category.objects.all()

        product_context_details = {
            'product': product,
            'brands':brands,
            'categories':categories
        }
        return render(request, 'admin_side/edit-products.html', product_context_details)
    return redirect('admin_app:admin_login')



def deactivate_product(request,id):
    product = get_object_or_404(Product, id=id)
    product.is_available = False
    product.save()
    return redirect('product_management_app:admin_products_list')

def activate_product(request,id):
    product = get_object_or_404(Product, id=id)
    product.is_available = True
    product.save()
    return redirect('product_management_app:admin_products_list')


def show_actived_products(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.filter(is_available=True).order_by('id')
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context = {
            'products':products,
            'categories':categories,
            'brands':brands,
        }
        print('hello')
        return render(request,'admin_side/page-products-list.html',context)
    return redirect('admin_app:admin_login')


def show_inactive_products(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.filter(is_available=False).order_by('id')
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context = {
            'products':products,
            'categories':categories,
            'brands':brands,
        }
        print('hello')
        return render(request,'admin_side/page-products-list.html',context)
    return redirect('admin_app:admin_login')   



def add_extra_images(request):
    return render(request, 'admin_side/additional-images.html')



@never_cache
def activate_brand(request, id):
    current = get_object_or_404(Brand, id=id)
    current.is_active = True
    current.save()
    return redirect('category_app:create_brand')                     

@never_cache
def deactivate_brand(request, id):
    current = get_object_or_404(Brand, id=id)
    current.is_active = False
    current.save()
    return redirect('category_app:create_brand') 


                        
