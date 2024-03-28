from django.shortcuts import render,redirect
from admin_app.models import User
from django.views.decorators.cache import cache_control,never_cache
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from admin_app.decorators import admin_login_required





@admin_login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            users = User.objects.filter(is_superuser = False).order_by('id')
            paginator = Paginator(users,6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page) 
            user_all = {
                'users':paged_products
            }
            return render(request,'admin_side/page-users-list.html',user_all)
        return redirect('admin_app:admin_login')

@admin_login_required
def search_user(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            if request.method == 'POST':
                uname = request.POST["search"]
                if uname != '':
                    
                    users = User.objects.filter(username__istartswith = uname)
                    user_all = {
                        'users':users
                    }
                    return render(request, 'admin_side/page-users-list.html',user_all)
                else:
                    return redirect('user_management_app:users_list')
                
@admin_login_required
def edit_user(request,id):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            user = User.objects.get(id = id)
            if request.method == 'POST':
             
                is_active = request.POST.get("is_active")

               
                
                if is_active:
                    is_active = bool(int(is_active))
                    user.is_active = is_active

                user.save()
                messages.success(request,"User updated Successfully")
                return redirect('user_management_app:users_list')
            
            context = {
                'user':user
            }
            return render(request,'admin_side/edit-user.html',context)
        else:
            return render(request,'admin_side/edit-user.html')
    else:
        return render(request,'userside/userlogin.html')
    
@admin_login_required
@never_cache
def activate_user(request, id):
    current = get_object_or_404(User, id=id)
    current.is_active = True
    current.save()
    return redirect('user_management_app:users_list')


@admin_login_required
@never_cache
def deactivate_user(request, id):
    current = get_object_or_404(User, id=id)
    current.is_active = False
    current.save()
    return redirect('user_management_app:users_list')


  

                