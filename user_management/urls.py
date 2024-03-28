from django.urls import path
from . import views

app_name = 'user_management_app'
urlpatterns = [

        path('users-list/',views.users_list,name='users_list'),
        path('search-user/',views.search_user,name='search_user'),
        path('edit-user/<int:id>/',views.edit_user,name='edit_user'),
        path('user-activate/<int:id>',views.deactivate_user,name='deactivate_user'),
        path('user-deactivate/<int:id>',views.activate_user,name='activate_user'),







]