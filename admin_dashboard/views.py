from django.shortcuts import render,redirect
import datetime
from orders.models import Order,OrderProduct
from store.models import Banner
from django.contrib import messages
from admin_app.decorators import admin_login_required


@admin_login_required
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_app:admin_login')
    start_date_value = ""
    end_date_value = ""
    try:
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        orders=Order.objects.filter(is_ordered = True).order_by('-created_at')
        order_products = OrderProduct.objects.filter(order__payment__payment_status__in=["SUCCESS"], order_status__in=["Delivered", "Accepted", "New"])

        total_amount = 0
        for i in order_products:
            total_amount += i.grand_totol

    except Exception as e:
        print("its exception",str(e))
        
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

           
            order_products = order_products.filter(created_at__range=(start_date, end_date))
            total_amount = 0
            for i in order_products:
                total_amount += i.grand_totol
   
    context={
        'orders':order_products,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value,
        'total_amount':total_amount
    }

    return render(request,'admin_side/sales_report.html',context)



@admin_login_required
def banner(request):
    banners = Banner.objects.all()
    if request.method == 'POST':
        # Handle form submission for creating a new banner
        banner_title = request.POST.get('banner_title')
        banner_image = request.FILES.get('banner_image')
        is_visible = request.POST.get('is_visible')
        banner_caption = request.POST.get('banner_caption')


        if is_visible == None:
            is_visible = False  
        else:
            is_visible = True
        # Create the banner instance and save to database
        banner = Banner.objects.create(banner_title=banner_title, images=banner_image, is_visible=is_visible,banner_caption = banner_caption)
        banner.save()
        messages.success(request,"Banner Created Successfully")

    context = {
        "banners":banners,
    }
    

    return render(request,'admin_side/banner/banners.html',context)


@admin_login_required
def edit_banner(request, id):
    banner = Banner.objects.get(id=id)

    if request.method == 'POST':
        banner_title = request.POST.get('edit_banner_title')
        banner_caption = request.POST.get('banner_caption')
        banner_image = request.FILES.get('edit_banner_image')
        is_visible = request.POST.get('edit_is_visible')

        # Check if 'is_visible' checkbox is checked
        is_visible = is_visible == 'on'

        # Update fields if they are not empty
        if banner_image:
            banner.images = banner_image
        if banner_title:
            banner.banner_title = banner_title
        
        if banner.banner_caption:
            banner.banner_caption = banner_caption
        banner.is_visible = is_visible
        banner.save()

        messages.success(request, 'Banner Modified Successfully')
        return redirect("admin_dashboard:banner")

    return render(request, "admin_side/banner/edit_banner.html", {"banner": banner})


def delete_banner(request,id):

    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect("admin_dashboard:banner")




