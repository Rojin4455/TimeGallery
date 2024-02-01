from django.urls import path
from . import views

urlpatterns = [
    path('userlogin/', views.userlogin, name='userlogin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('',views.userhome, name = 'home'),
    path('check-otp/',views.check_otp, name = 'check-otp'),
    path('user-logout/',views.user_logout, name = 'user-logout'),



]
