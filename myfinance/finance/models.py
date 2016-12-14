from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import RegexValidator


# Create your models here.


class UserProfile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                         " '+999999999'. Up to 15 digits allowed."
                                 )
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16)
    address = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(User, related_name='profile')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Account(models.Model):
    number = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, default='empty account name')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Charge(models.Model):
    account = models.ForeignKey(Account, related_name='charges', on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=9)
    date = models.DateField(default=timezone.now)


