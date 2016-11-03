import datetime
from django.utils import timezone
from django import forms


class ChargeForm(forms.Form):
    value = forms.DecimalField(label='Value', required=False)
    date = forms.DateField(initial=datetime.date.today())

    def clean(self):
        cleaned_data = super().clean()

        value = self.cleaned_data.get('value')
        date = self.cleaned_data.get('date')
        if date and date > datetime.date.today():
            self.add_error('date', 'Must be early than today')

        if value < 0:
            self.add_error('value', 'Must be positive')

        return cleaned_data

