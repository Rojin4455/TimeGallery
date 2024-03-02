
from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from store.models import Product,Brand,Product_Variant,Attribute_Value
from category.models import Category
from django.views.decorators.cache import cache_control,never_cache
from django.shortcuts import get_object_or_404
from store.models import Additional_Product_Image
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from store.models import Attribute_Value
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from admin_app.decorators import admin_login_required
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator



@admin_login_required
@never_cache
def admin_products_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all().order_by('id')
        categories = Category.objects.all()
        brands = Brand.objects.all()

        paginator = Paginator(products,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
          
        context = {
            'products':paged_products,
            'categories':categories,
            'brands':brands,
        }
        return render(request,'admin_side/page-products-list.html',context)
    return redirect('admin_app:admin_login')

@admin_login_required
@never_cache
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        print("before entering post method")
        if request.method == 'POST':
            title = request.POST.get('product_title')
            # stock_qty = request.POST.get('stock_qty')
            brand_id = request.POST.get('Brand')
            description = request.POST.get('description')
            # price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            base_price = request.POST.get('base_price')
            print("entering post method")
            image = request.FILES.get('image')
            # additional_images = request.FILES.getlist('additional_image_1')


            # try:
            #     # image = request.FILES.get('image')
            # except :
            #     messages.warning(request,"add product image")
            #     return redirect('product_management_app:add_product') 

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
                # stock = stock_qty,
                brand = brand,
                category = category,
                description = description,
                # price = price,
                # images = image,
                base_price = base_price
            )
            product.save()
            
            # for img in additional_images:
            #     Additional_Product_Image.objects.create(product=product,image=img)    
            return redirect('product_management_app:admin_products_list')

        categories = Category.objects.filter(is_active = True)
        brands = Brand.objects.filter(is_active = True)
        context = {
            'categories':categories,
            'brands':brands
        }
            
        return render(request,'admin_side/page-form-product-3.html',context)
    return redirect('admin_app:admin_login')




@admin_login_required
@never_cache
def edit_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=id)

        if request.method == 'POST':
            title = request.POST.get('product_title')
            # stock_qty = request.POST.get('stock_qty')
            # brand_id = request.POST.get('brand')
            brand_id = request.POST.get('brand')
            brand = get_object_or_404(Brand, pk=brand_id)
            description = request.POST.get('description')
            # price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, pk=category_id)
            print("entering post method")
            # image = request.FILES.get('image')
            # additional_images = request.FILES.getlist('additional_image_1')
            
            if title:
                product.product_name = title
            # if stock_qty:
            #     product.stock = stock_qty
            if brand_id:
                product.brand = brand
            if description:
                product.description = description
            # if price:
            #     product.price = price
            if category_id:
                product.category = category


            # if image:
            #     product.images = image
            # for img in additional_images:
            #     Additional_Product_Image.objects.create(product=product,image=img)  

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



@admin_login_required
def deactivate_product(request,id):
    product = get_object_or_404(Product, id=id)
    product.is_available = False
    product.save()
    return redirect('product_management_app:admin_products_list')



@admin_login_required
def activate_product(request,id):
    product = get_object_or_404(Product, id=id)
    product.is_available = True
    product.save()
    return redirect('product_management_app:admin_products_list')



@admin_login_required
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



@admin_login_required
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




@admin_login_required
def add_extra_images(request):
    return render(request, 'admin_side/additional-images.html')




@admin_login_required
@never_cache
def activate_brand(request, id):
    current = get_object_or_404(Brand, id=id)
    current.is_active = True
    current.save()
    return redirect('category_app:create_brand')                     


@admin_login_required
@never_cache
def deactivate_brand(request, id):
    current = get_object_or_404(Brand, id=id)
    current.is_active = False
    current.save()
    return redirect('category_app:create_brand') 

# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Product, Attribute_Value



@admin_login_required
def add_product_variant(request,id):
    if request.method == 'POST':
        print('its under post')
        # sku_id = request.POST.get('sku_id')
        variant_name = request.POST.get('variant_name')
        max_price = request.POST.get('max_price')
        sale_price = request.POST.get('sale_price')
        stock = request.POST.get('stock')
        # product_id = request.POST.get('product')
        product = get_object_or_404(Product, pk=id)

        attribute_id = request.POST.get('attributes')
        attribute = get_object_or_404(Attribute_Value, pk=attribute_id)
        # is_active = request.POST.get('is_active')


        thumbnail_image = request.FILES.get('image')

        additional_images = request.FILES.getlist('additional_image_1')

        # Create the Product_Variant object
        p = Product_Variant.objects.create(
            # sku_id=sku_id,
            max_price=max_price,
            variant_name=variant_name,
            stock=stock,
            sale_price=sale_price,
            product=product,
            thumbnail_image=thumbnail_image,
        )   

        # Add the attribute to the Product_Variant
        p.attributes.add(attribute)
        p.save()
        for image in additional_images:
            # Create and save Additional_Product_Image object
            additional_image = Additional_Product_Image(
                product_variant=p,
                image=image,
            )
            additional_image.save()
            return redirect(reverse('product_management_app:product-variant-list', kwargs={'id': product.id}))
        print('Product Variant created successfully')
        # Redirect or render a success message

    # Get products and attribute values for the form
    products = Product.objects.get(pk=id)
    attribute_values = Attribute_Value.objects.filter(is_active=True)

    context = {
        'products': products,
        'attribute_values': attribute_values
    }

    return render(request, 'admin_side/add-product-variant.html', context)



@admin_login_required
def product_variant_list(request,id):
    product_variants = Product_Variant.objects.filter(product=id)
    # product_variants = get_object_or_404(Product_Variant,Product=id)
    selected_product = Product.objects.get(id=id)
    context = {
        'product_variants':product_variants,
        'selected_product':selected_product
    }
    return render(request, 'admin_side/product-variant-list.html',context)


from django.db import IntegrityError
from django.shortcuts import redirect



@admin_login_required
def attribute_values(request):
    if request.method == "POST":
        attribute_value = request.POST.get('attribute_value')
        slug = request.POST.get('slug')
        
        # Check if the 'is_active' field is present in the POST data
        is_active = request.POST.get('is_active', True)
        # Convert the value to a boolean if it's not None
        if is_active is not None:
            is_active = is_active == 'on'

        # Check if an Attribute_Value object with the same attribute_value already exists
        if Attribute_Value.objects.filter(attribute_value=attribute_value).exists():
            messages.error(request, "Attribute Value already exists")
            return redirect('product_management_app:attribute-values')

        # Create the attribute value object
        try:
            attribute = Attribute_Value.objects.create(attribute_value=attribute_value, slug=slug, is_active=is_active)
            messages.success(request, "Attribute value created")

            # Optionally, you can redirect to a different page after successful creation
            # return redirect('product_management:attribute_values')
        except IntegrityError as e:
            messages.error(request, "Error creating Attribute Value: {}".format(str(e)))

    attribute_values = Attribute_Value.objects.all().order_by('id')
    context = {
        'attribute_values': attribute_values
    }
    return render(request, 'admin_side/add-variant-attribute.html', context)


# @require_POST
# def block_attribute_value(request, attribute_value_id):
#     try:
#         attribute_value = Attribute_Value.objects.get(pk=attribute_value_id)
#         is_active = request.POST.get('is_active', False)
#         if is_active is not None:
#             is_active = is_active == 'true'  # Convert string to boolean

#         attribute_value.is_active = is_active
#         attribute_value.save()
#         return HttpResponse('Attribute value status updated successfully', status=200)
#     except Attribute_Value.DoesNotExist:
#         return HttpResponse('Attribute value not found', status=404)
#     except Exception as e:
#         return HttpResponse(f'Error: {str(e)}', status=500)


@admin_login_required
@never_cache
def deactivate_attribute(request,id):
    current = get_object_or_404(Attribute_Value, id=id)
    current.is_active = False
    current.save()
    return redirect('product_management_app:attribute-values')

@admin_login_required
@never_cache
def activate_attribute(request,id):
    current = get_object_or_404(Attribute_Value, id=id)
    current.is_active = True
    current.save()
    return redirect('product_management_app:attribute-values')


@admin_login_required
def edit_product_variant(request, id):
    product_variant = get_object_or_404(Product_Variant, id=id)
    variants = Attribute_Value.objects.all()
    product_variant = get_object_or_404(Product_Variant, id=id)
    a= product_variant.product
    print(a)
    if request.method == "POST":
        sku_id = request.POST.get('sku_id')
        max_price = request.POST.get('max_price')
        variant_name = request.POST.get('variant_name')
        sale_price = request.POST.get('sale_price')
        stock = request.POST.get('stock')
        color_ids = request.POST.getlist('color')  # Use getlist for multiple selections
        is_active = request.POST.get('is_active')
        thumbnail_image = request.FILES.get('thumbnail_image')
        additional_image_1 = request.FILES.getlist('additional_image_1')


        if sku_id:
            product_variant.sku_id = sku_id
        if max_price:
            product_variant.max_price = max_price
        if sale_price:
            product_variant.sale_price = sale_price
        if stock:
            product_variant.stock = stock
        if is_active:
            is_active = bool(int(is_active))  # Convert to boolean
            product_variant.is_active = is_active
        if variant_name:
            product_variant.variant_name=variant_name

        # Clear existing colors and add selected colors
        product_variant.attributes.clear()
        for color_id in color_ids:
            color_instance = Attribute_Value.objects.get(id=color_id)
            product_variant.attributes.add(color_instance)

        if thumbnail_image:
            product_variant.thumbnail_image = thumbnail_image

        if additional_image_1:
            for image in additional_image_1:
                Additional_Product_Image.objects.create(product_variant=product_variant,image=image)
        product_variant.save()
        return redirect(reverse('product_management_app:product-variant-list', kwargs={'id': product_variant.product.id}))


        # Redirect to a success page or back to the product variant detail page
        # Example: return redirect('product_variant_detail', id=product_variant.id)

    context = {
        'product_variant': product_variant,
        'variants': variants
    }
    return render(request, 'admin_side/edit-product-variant.html', context)



@admin_login_required
def delete_product_variant(request,id):
    product_variant = Product_Variant.objects.get(id=id)
    product = product_variant.product
    product_variant.delete()

    return redirect(reverse('product_management_app:product-variant-list', kwargs={'id': product.id}))

    



                        
