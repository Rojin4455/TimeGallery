from django.shortcuts import render
from .models import Account
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.contrib.auth import authenticate

@never_cache
def usersignup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        Email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if Account.objects.filter(email = Email).exists():
            messages(request,'Email Already Exists')
        elif pass1 != pass2:
            messages(request,"Password Does not Match")
        else:
            user1 = Account.objects.create(firstname = first_name, lastname = last_name, email = Email,password = pass1)
            user1.is_active = False
            user1.is_admin = False
            user1.is_superadmin = False
            user1.is_staff = False
            user1.is_superuser = False

            user1.save()
            return render(request, 'home.html')
    # return render(request,'userlogin.html')

def userlogin(request):

    if request.method == 'POST':
        Email = request.POST.get('email')
        Pass = request.POST.get('password')
        user_details = authenticate(email = Email, password = Pass)
        if user_details is not None and user_details.is_superuser is False:
            return HttpResponse(request, '<h1>Welcome User</h1>')
        else:
            return HttpResponse(request, 'Something Went Wrong Please Try Again...')
    # return render(request,'userside/userlogin.html')
    return HttpResponse(request, 'Something Went Wrong Please Try Again...')





            
