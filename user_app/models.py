from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractBaseUser

# class Account(AbstractBaseUser):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, default = None)

#     #required
#     date_join       = models.DateTimeField(auto_now_add=True)
#     last_login      = models.DateTimeField(auto_now_add=True)
#     is_admin        = models.BooleanField(default=False)
#     is_staff        = models.BooleanField(default=False)
#     is_active       = models.BooleanField(default=False)
#     is_superadmin   = models.BooleanField(default=False)
#     is_blocked      = models.BooleanField(default=False)
#     is_superuser    = models.BooleanField(default=False)

class User(AbstractBaseUser):
    is_email_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.email
