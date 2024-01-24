from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Account(AbstractBaseUser):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length=150, unique = True)

    #required
    date_join      = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_blocked        = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

