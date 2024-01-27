from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

@never_cache
def usersignup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(username)
        print(email)
        print(password1)
        print(password2)

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already Exists')
        elif password1 != password2:
            messages.warning(request, "Passwords Do Not Match")
        else:
            user1 = User.objects.create(username=username, email=email, password=password1)
            # user1.is_active = False
            # user1.is_admin = False
            # user1.is_superadmin = False
            # user1.is_staff = False
            # user1.is_superuser = False
            user1.save()
            return redirect("home")
            # login(request,user1)
            # return render(request, 'userside/userlogin.html')

    else:
        return render(request, 'userside/usersignup.html')


@never_cache
def userlogin(request):

    print('userlogin')
    # if request.user.is_authenticated:
    #     return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        # user_details = authenticate(username=username, password=password)

        # if user_details is not None:
        if User.objects.filter(Q(username = username) & Q(password = password)).exists():
            # login(request, user_details)
            return redirect("home")
        else:
            messages.error(request, 'Invalid Credentials. Please Try Again.')
            return redirect('userlogin')

    return render(request, 'userside/userlogin.html')


def userhome(request):
    return render(request, 'userside/home.html')
