from django.shortcuts import render,redirect
from django.contrib import messages
from store.models import Product,Brand
from category.models import Category



def admin_products_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context = {
            'products':products,
            'categories':categories,
            'brands':brands,
        }
        return render(request,'admin_side/page-products-list.html',context)
    return redirect('admin_app:admin_login')



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
            messages.success(request, 'Product Added.')
            

        categories = Category.objects.filter(is_active = True)
        brands = Brand.objects.filter(is_active = True)
        context = {
            'categories':categories,
            'brands':brands
        }
        return render(request,'admin_side/page-form-product-3.html', context)
    return redirect('admin_app:admin_login')
