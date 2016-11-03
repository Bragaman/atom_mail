from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from random import randint
from finance.forms import *


def home_page(request):
    return render(request, 'home_page.html')


def charges_page(request):
    def random_transactions():
        today = date.today()
        start_date = today.replace(month=1, day=1).toordinal()
        end_date = today.toordinal()
        while True:
            start_date = randint(start_date, end_date)
            random_date = date.fromordinal(start_date)
            if random_date >= today:
                break
            random_value = randint(-10000, 10000), randint(0, 99)
            random_value = Decimal('%d.%d' % random_value)
            yield random_date, random_value

    gen = random_transactions()
    charges = [c for c in gen]
    return render(request, 'charges_page.html', {'charges': charges})


# @require_POST
def add_charge(request):
    if request.method == "POST":
        form = ChargeForm(request.POST)  # if no files
        if form.is_valid():
            # do something if form is valid
            return render(request, 'finish_charge.html')
    else:
        form = ChargeForm()
    return render(request, 'add_charge.html', {'form': form})
