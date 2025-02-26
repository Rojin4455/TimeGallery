from django.urls import path
from . import views

app_name = 'category_app'

urlpatterns = [

    path('categories/',views.categories,name='categories'),
    path('edit-category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),

    # brand management
    path('create-brand/',views.create_brand,name='create_brand'),
    path('delete-brand/<int:id>/',views.delete_brand,name='delete_brand'),
    path('category_offer/',views.category_offer,name='category_offer'),
    path('deactivate_category_offer/<int:id>/',views.deactivate_category_offer,name='deactivate_category_offer'),
    path('delete_category_offer/<int:id>/',views.delete_category_offer,name='delete_category_offer'),



]