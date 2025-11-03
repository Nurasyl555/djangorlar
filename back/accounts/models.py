from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address", unique=True)
    first_name = models.CharField("First Name", max_length=30, blank=True)
    last_name = models.CharField("Last Name", max_length=30, blank=True)

    is_staff = models.BooleanField("Staff Status", default=False)
    is_active = models.BooleanField("Active", default=True)
    date_joined = models.DateTimeField("Date Joined", default=timezone.now)

    USER_NAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def get_short_name(self):
        return self.first_name


    