from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('sales_report/',views.sales_report,name='sales_report'),
    path('banner/',views.banner,name='banner'),
    path('edit_banner/<int:id>/',views.edit_banner,name='edit_banner'),
    path('delete_banner/<int:id>/',views.delete_banner,name='delete_banner')


]