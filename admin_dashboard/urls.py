from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('sales_report',views.sales_report,name='sales_report')

]