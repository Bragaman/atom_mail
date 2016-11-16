import datetime

from django import forms
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
        fields = ['account', 'value', 'date']

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
