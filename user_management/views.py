from django.shortcuts import render,redirect
from admin_app.models import User
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.contrib import messages




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            users = User.objects.filter(is_superuser = False)
            user_all = {
                'users':users
            }
            return render(request,'admin_side/page-users-list.html',user_all)
        return redirect('admin_app:admin_login')

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
                

def edit_user(request,id):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            user = User.objects.get(id = id)
            if request.method == 'POST':
                # uname = request.POST.get("username")
                # email = request.POST.get("email")
                is_active = request.POST.get("is_active")

                # if uname:
                #     user.username = uname

                # if email:
                #     user.email = email
                
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
                        

                        
                    

                