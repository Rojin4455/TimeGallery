from django.urls import path
from . import views

app_name = 'user_app'
urlpatterns = [
    path('usersignup/', views.signup, name='usersignup'),
    path('',views.userhome, name = 'userhome'),
    path('check-otp/',views.otp, name = 'check-otp'),
    path('login/', views.login, name='login'),
    path('logout',views.logout, name='user_logout'),



    path('account_settings',views.account_settings,name='account_settings'),
    path('profile-details',views.profile_details,name='profile-details'),
    path('base-profile',views.base_profile,name='base_profile'),
    path('profile-address',views.profile_address,name='profile-address'),
    path('profile-orders',views.profile_orders,name='profile-orders'),
    path('create-address',views.create_address,name='create_address'),
    path('edit-address/<int:id>/',views.edit_address,name='edit_address'),
    path('edit-address/',views.delete_address,name='deleteaddress'),
    path('upload-profile-image', views.upload_profile_image, name='upload-profile-image'),


    path('set-default-address/', views.set_default_address, name='set_default_address'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password_otp/', views.forgot_password_otp, name='forgot_password_otp'),


    







]
