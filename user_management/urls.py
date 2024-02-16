from django.urls import path
from . import views

app_name = 'user_management_app'
urlpatterns = [

        path('users-list/',views.users_list,name='users_list'),
        path('search-user/',views.search_user,name='search_user'),
        path('edit-user/<int:id>/',views.edit_user,name='edit_user'),
        path('user-activate/<int:id>',views.deactivate_user,name='deactivate_user'),
        path('user-deactivate/<int:id>',views.activate_user,name='activate_user'),
        # path('account_settings',views.account_settings,name='account_settings'),
        # path('profile-details',views.profile_details,name='profile-details'),
        # path('base-profile',views.base_profile,name='base_profile'),
        # path('profile-address',views.profile_address,name='profile-address'),
        # path('profile-orders',views.profile_orders,name='profile-orders'),






]