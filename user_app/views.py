# # from django.shortcuts import render, redirect
# # from django.contrib import messages
# # from django.views.decorators.cache import never_cache
# # from django.contrib.auth import authenticate, login, logout
# # from django.http import HttpResponse
# # from django.contrib.auth.models import User
# # from django.db.models import Q
# # from django.contrib.sites.shortcuts import get_current_site
# # from django.template.loader import render_to_string
# # from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# # from django.utils.encoding import force_bytes,force_str,force_text,DjangoUnicodeDecodeError
# # from .utils import generate_token
# # from django.urls import reverse
# # from django.core.mail import EmailMessage
# # from django.conf import settings

# # def send_action_email(user,request):
# #     current_site = get_current_site(request)
# #     email_subject = 'Activate your account'
# #     email_body = render_to_string('userside/activate.html',
# #                                   {'user' : user,
# #                                    'domain': current_site,
# #                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# #                                    'token': generate_token.make_token(user)
# #                                    })
    
# #     EmailMessage(subject=email_subject,body=email_body,
# #                  from_email=settings.EMAIL_FROM_USER,
# #                  to=[user.email]             
# #                  )

# #     email.send()

# # @never_cache
# # def usersignup(request):
# #     # if request.user.is_authenticated:
# #     #     return redirect("home")

# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         email = request.POST.get('email')
# #         password1 = request.POST.get('password1')
# #         password2 = request.POST.get('password2')
# #         print(username)
# #         print(email)
# #         print(password1)
# #         print(password2)

        


# #         if User.objects.filter(email=email).exists():
# #             messages.warning(request, 'Email Already Exists')
# #         elif password1 != password2:
# #             messages.warning(request, "Passwords Do Not Match")
# #         else:
# #             user1 = User.objects.create(username=username, email=email, password=password1)
# #             # user1.is_active = False
# #             # user1.is_admin = False
# #             # user1.is_superadmin = False
# #             # user1.is_staff = False
# #             # user1.is_superuser = False
# #             user1.save()

# #             send_action_email(user1,request)
# #             return redirect("home")
# #             # login(request,user1)
# #             # return render(request, 'userside/userlogin.html')

# #     else:
# #         return render(request, 'userside/usersignup.html')


# # @never_cache
# # def userlogin(request):

# #     print('userlogin')
# #     # if request.user.is_authenticated:
# #     #     return redirect('home')

# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')
# #         print(username)
# #         # user_details = authenticate(username=username, password=password)

# #         # if user_details is not None:

# #         user = authenticate(username=username, password=password)

# #         if not user.is_email_verified:
# #             messages.add_message(request, messages.ERROR,
# #                                  'Email is not verified, please check your email inbox')
# #             return render(request,'userside/userlogin.html')
        

# #         if User.objects.filter(Q(username = username) & Q(password = password)).exists():
# #             # login(request, user_details)
# #             return redirect("home")
# #         else:
# #             messages.error(request, 'Invalid Credentials. Please Try Again.')
# #             return redirect('userlogin')

# #     return render(request, 'userside/userlogin.html')


# # def userhome(request):
# #     return render(request, 'userside/home.html')


# # def activate_user(request,uidb64, token):
# #     try:
# #         uid = force_text(urlsafe_base64_decode(uidb64))
# #         user = User.objects.get(pk = uid)
# #     except Exception as e:
# #         user = None
# #     if user and generate_token.check_token(user,token):
# #         user.is_email_verified = True
# #         user.save()

# #         messages.add_message(request,messages.SUCCESS,'Email verified, you can login')
# #         return redirect(reverse('login'))
# #     return render(request,'userside/activate_faild.html', {'user':user})





# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.views.decorators.cache import never_cache
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.db.models import Q
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from .utils import generate_token
# from django.urls import reverse

# from django.core.mail import EmailMessage
# from django.conf import settings

# def send_action_email(user, request):
#     current_site = get_current_site(request)
#     email_subject = 'Activate your account'
#     email_body = render_to_string('userside/activate.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': generate_token.make_token(user),
#     })

#     email = EmailMessage(
#         subject=email_subject,
#         body=email_body,
#         from_email=settings.EMAIL_FROM_USER,
#         to=[user.email],
#     )

#     email.send()

# @never_cache
# def usersignup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if User.objects.filter(email=email).exists():
#             messages.warning(request, 'Email Already Exists')
#         elif password1 != password2:
#             messages.warning(request, "Passwords Do Not Match")
#         else:
#             user1 = User.objects.create_user(username=username, email=email, password=password1)
#             user1.is_active = False
#             user1.save()

#             send_action_email(user1, request)
#             return redirect("home")

#     return render(request, 'userside/usersignup.html')

# @never_cache
# def userlogin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if not user.is_email_verified:
#             messages.add_message(request, messages.ERROR,
#                                  'Email is not verified, please check your email inbox')
#             return render(request, 'userside/userlogin.html')

#         if user:
#             login(request, user)
#             return redirect("home")
#         else:
#             messages.error(request, 'Invalid Credentials. Please Try Again.')
#             return redirect('userlogin')

#     return render(request, 'userside/userlogin.html')

# def userhome(request):
#     return render(request, 'userside/home.html')

# def activate_user(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))

#         user = User.objects.get(pk=uid)
#     except Exception as e:
#         user = None

#     if user and generate_token.check_token(user, token):
#         user.is_active = True
#         user.save()

#         messages.add_message(request, messages.SUCCESS, 'Email verified, you can login')
#         return redirect(reverse('userlogin'))
#     return rende
# r(request, 'userside/activate_failed.html', {'user': user})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
import random 
from django.core.mail import send_mail







@never_cache
def usersignup(request):
    # if request.user.is_authenticated:
    #     return redirect("home")

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

        randomotp = str(random.randint(1000, 9999))
        request.session['storedotp'] = randomotp
        request.session['storedemail']=email
        request.session.modified = True 
        request.session.set_expiry(300)

        subject = "Verify Your One-Time Password (OTP) - Time Gallery Ecommerce Store"
        sendermail = "timegalleryt.com"
        otp = f"Hello,\n\nYour One-Time Password (OTP) for verification at Time Gallery Ecommerce Store is: {randomotp}\n\nThank you for choosing Time Gallery Ecommerce Store.\n\nBest regards,\nTime Gallery Ecommerce Store Team"

        send_mail(subject,otp,sendermail,[email])

        return render(request,'userside/otp.html')


            # login(request,user1)
            
            # login(request,user1)
            # return render(request, 'userside/userlogin.html')

    else:
        return render(request, 'userside/usersignup.html')


def check_otp(request):
    if request.method == 'POST':
        entered_otp = ''.join(request.POST.get(f'otp{i}', '') for i in range(1, 5))
        storedotp=request.session['storedotp']
        storedemail = request.session['storedemail']

        if entered_otp == storedotp:
            user = User.objects.get(email=storedemail)
            user.is_active = True
            user.save()
            subject = "Successful Login - Time Gallery Ecommerce Store"
            sender_mail = "timegalleryt.com"
            message = "Hello,\n\nThank you for logging into Time Gallery Ecommerce Store.\n\nWe appreciate your continued support.\n\nBest regards,\nTime Gallery Ecommerce Store Team"
            

            send_mail(subject, message, sender_mail,[storedemail])
            # login(request,user)
            return redirect ('home')
    
    return render(request,'userside/otp.html')


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

        user = authenticate(username=username, password=password)

        if request.user.is_authenticated:
        # if User.objects.filter(Q(username=username) & Q(password=password)).exists():
            # login(request, user_details)
            return redirect("home")
        else:
            messages.error(request, 'Invalid Credentials. Please Try Again.')
            return redirect('userlogin')

    return render(request, 'userside/userlogin.html')

@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,("You Were Logged Out!"))
    return redirect('userlogin')


def userhome(request):
    if request.user.is_authenticated:
        return render(request, 'userside/home.html')

    return render(request, 'userside/home.html')


