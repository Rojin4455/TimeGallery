from django.urls import path
from . import views

urlpatterns = [
    path('usersignin/', views.userlogin, name='userlogin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('',views.userhome, name = 'home'),
]
