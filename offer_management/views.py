from django.shortcuts import render, redirect
from .models import ReferralOffer, ReferralUser
from django.contrib import messages
import string
import random
from decimal import Decimal


def referral_offer(request):
    if request.method == 'POST':
        print("podpad")
        expire_date = request.POST.get('expire_date')
        print(expire_date)
        amount = request.POST.get('amount')
        print(type(amount))
        limit = request.POST.get('limit')
        print(limit)
        is_active = request.POST.get('is_active', False)
        print(is_active)
        amount = Decimal(amount)
        # Convert is_active to boolean
        is_active = True if is_active == 'on' else False
        print(is_active)

        try:
            # Create the ReferralOffer object
            ReferralOffer.objects.create(
                expire_date=expire_date,
                amount=amount,
                limit=limit,
                is_active=is_active
            )
            print("created")
            messages.success(request, 'Referral Offer created successfully.')
            return redirect('offer_management_app:referral_offer')
        except Exception as e:
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",str(e))
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('offer_management_app:referral_offer')

    referral_offers = ReferralOffer.objects.all()
    context = {
        'referral_offers': referral_offers,
    }
    # If it's a GET request, render the form template
    return render(request, 'admin_side/referral_offer.html',context)

def change_offer_status(request,id):
    try:
        offer = ReferralOffer.objects.get(id=id)
        if offer.is_active == True:
            offer.is_active = False
        else:
            offer.is_active = True
        offer.save()

    except:
        messages.error(request,"Something Went Wrong")
        pass

    return redirect('offer_management_app:referral_offer')


def delete_referral_offer(request,id):
    try:
        offer = ReferralOffer.objects.get(id = id)
        offer.delete()

    except:
        messages.error(request,"Something Went Wrong")
        pass

    return redirect('offer_management_app:referral_offer')