import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from finance.models import *


class ChargeFormNoModel(forms.Form):
    value = forms.DecimalField(label='Value', required=False)
    date = forms.DateField(initial=datetime.date.today())

    def clean(self):
        cleaned_data = super().clean()

        value = self.cleaned_data.get('value')
        date = self.cleaned_data.get('date')
        if date and date > datetime.date.today():
            self.add_error('date', 'Must be early than today')

        if value and value < 0:
            self.add_error('value', 'Must be positive')

        return cleaned_data


class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = ['value', 'date']

    def clean(self):
        cleaned_data = super().clean()

        date = self.cleaned_data.get('date')
        if date and date > datetime.date.today():
            self.add_error('date', 'Must be early than today')

        return cleaned_data


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'number']


class ProfileCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                         " '+999999999'. Up to 15 digits allowed."
                                 )
    phone_number = forms.CharField(max_length=16,
                                   validators=[phone_regex,])

    address = forms.CharField(max_length=500,
                              widget=forms.Textarea)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = super(ProfileCreateForm, self).save()
        user.email = self.cleaned_data["email"]
        user.profile.phone_number = self.cleaned_data["phone_number"]
        user.profile.address = self.cleaned_data["address"]
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                         " '+999999999'. Up to 15 digits allowed."
                                 )
    phone_number = forms.CharField(max_length=16,
                                   validators=[phone_regex, ])

    address = forms.CharField(max_length=500,
                              widget=forms.Textarea)

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self):
        user = super(ProfileUpdateForm, self).save()
        user.profile.phone_number = self.cleaned_data["phone_number"]
        user.profile.address = self.cleaned_data["address"]
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address', 'phone_number',)

