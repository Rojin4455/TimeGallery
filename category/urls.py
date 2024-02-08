from django.urls import path
from . import views

app_name = 'category_app'

urlpatterns = [

    path('categories/',views.categories,name='categories'),
    path('edit-category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),




]