from django.shortcuts import render,redirect
import datetime
from orders.models import Order

def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_app:admin_login')
    start_date_value = ""
    end_date_value = ""
    try:

        orders=Order.objects.filter(is_ordered = True).order_by('-created_at')
        print(" ddddddddddddddddddddddd",orders)
    
    except:
        pass
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

           
            orders = orders.filter(created_at__range=(start_date, end_date))
   
    context={
        'orders':orders,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value
    }

    return render(request,'admin_side/sales_report.html',context)