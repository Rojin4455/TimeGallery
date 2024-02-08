from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
from django.utils.text import slugify




def categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            cat_name = request.POST.get('name','').strip()
            cat_slug = request.POST['slug']
            cat_image = request.FILES.get('image')
            cat_description = request.POST['description']
            if cat_name:
                print("Category have name")
                try:
                    if  Category.objects.get(cat_name=cat_name):
                        print("Category is takn")
                        messages.error(request,"Category is taken")
                        return redirect('admin_app:admin_categories')
                except:
                    pass   
                    
                print("Category is created")

                category = Category.objects.create(cat_name = cat_name,cat_slug = cat_slug, cat_image = cat_image, cat_description = cat_description)
                category.save()
                messages.success(request,"Category Created Successfully!", extra_tags="category_success")
        

        categories = Category.objects.all()
        category_context = {
            'categories':categories
        }
        return render(request,'admin_side/page-categories.html',category_context)
    return redirect('admin_app:admin_login')



def edit_category(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':

            category = Category.objects.get(id=id)

            cat_name = request.POST['name']

            cat_image = request.POST['image']
            cat_description = request.POST['description']
            is_active = request.POST.get("is_active")


            if cat_name:
                category.cat_name = cat_name
                category.cat_slug = slugify(cat_name)

            if cat_image:
                category.cat_image = cat_image
            if cat_description:
                category.cat_description = cat_description
            
            if is_active:
                is_active = bool(int(is_active))
                category.is_active = is_active
            
            category.save()
            messages.success(request,"Category updated",extra_tags="category_success")
            return redirect('category_app:categories')
        
        category_object = Category.objects.get(id=id)
        context = {
            'category_object':category_object
        }
        return render(request,'admin_side/edit-category.html',context)
    
    else:

        return redirect('admin_app:admin_login')
    

def delete_category(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_app:categories')


    



    








# Create your views here.
