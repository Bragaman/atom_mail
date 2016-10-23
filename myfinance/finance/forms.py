import datetime
from django import forms


class ChargeForm(forms.Form):

    value = forms.DecimalField(label='Value', required=True)
    date_value = forms.DateTimeField(initial=datetime.date.today)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('date_value') < datetime.date.today():
            self.add_error('date_value', 'Must be early than today')

        # if cleaned_data.get('value') < 0:
        #     self.add_error('value', 'Must be positive')

        return cleaned_data

