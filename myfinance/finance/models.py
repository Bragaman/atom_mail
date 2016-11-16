from django.db import models
import datetime

# Create your models here.


class Account(models.Model):
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=32, default='empty account name')

    def __str__(self):
        return self.name


class Charge(models.Model):
    account = models.ForeignKey(Account, related_name='charges', on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=9)
    date = models.DateField(default=datetime.date.today())
