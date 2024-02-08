from django.urls import path
from . import views

app_name = 'user_app'
urlpatterns = [
    # path('userlogin/', views.login, name='userlogin'),
    path('usersignup/', views.signup, name='usersignup'),
    path('',views.userhome, name = 'userhome'),
    path('check-otp/',views.otp, name = 'check-otp'),
    path('login',views.login,name='user_login'),
    path('logout',views.logout, name='user_logout'),
    # path('otp_verification',views.otp_verification,name="otp_verification"),





]
