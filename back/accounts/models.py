from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields you want for your custom user here
    bio = models.TextField("Биография", blank=True)
    phone_number = models.CharField("Номер телефона", max_length=15, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)

    def __str__(self):
        return self.username
