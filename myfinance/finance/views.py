from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from random import randint
from finance.forms import *


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
    return render(request, 'charges_fake_page.html', {'charges': charges})


def home_page(request):
    accounts = Account.objects.all()
    return render(request, 'home_page.html', {'accounts':accounts})


def account_charges(request, account_id):
    charges = Charge.objects.filter(account=account_id)
    print(len(charges))
    return render(request, 'charges_page.html', {'charges': charges, 'account_id': account_id})


# @require_POST
def add_charge_no_model(request):
    if request.method == "POST":
        form = ChargeFormNoModel(request.POST)  # if no files
        if form.is_valid():
            # do something if form is valid
            return render(request, 'finish_charge.html')
    else:
        form = ChargeFormNoModel()
    return render(request, 'add_from.html', {'form': form, 'path': '/add_charge_no_model/'})


def add_charge(request):
    if request.method == "POST":
        form = ChargeForm(request.POST)
        if form.is_valid():
            new_charge = form.save()
            new_charge.save()
            return render(request, 'finish_charge.html')
    else:
        form = ChargeForm()
    return render(request, 'add_from.html', {'form': form, 'path': '/add_charge/'})


def add_account_charge(request, account_id):
    if request.method == "POST":
        form = ChargeForm(request.POST, initial={'account': account_id})
        if form.is_valid():
            new_charge = form.save()
            new_charge.save()
            return render(request, 'finish_charge.html')
    else:
        form = ChargeForm(initial={'account': account_id})
    return render(request, 'add_from.html', {'form': form, 'path': '/add_charge/'})


def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'finish_charge.html')
    else:
        form = AccountForm()
    return render(request, 'add_from.html', {'form': form, 'path': '/add_account/'})
