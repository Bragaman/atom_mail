from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import datetime

# Create your models here.


class UserProfile(models.Model):
    phone_number = models.CharField(max_length=16)
    user = models.OneToOneField(User, related_name='profile')


class Account(models.Model):
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=32, default='empty account name')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts')

    def __str__(self):
        return self.name


class Charge(models.Model):
    account = models.ForeignKey(Account, related_name='charges', on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=9)
    date = models.DateField(default=timezone.now)


