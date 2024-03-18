from django.contrib import admin
from .models import CategoryOffer,ReferralOffer,ReferralUser

admin.site.register(CategoryOffer)
admin.site.register(ReferralOffer)
admin.site.register(ReferralUser)