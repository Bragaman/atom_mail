from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from finance.forms import *
from django.contrib.auth.decorators import login_required


@login_required
def home_page(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'home_page.html', {'accounts':accounts})

@login_required
def account_charges(request, account_id):
    charges = Charge.objects.filter(account=account_id)
    print(len(charges))
    return render(request, 'charges_page.html', {'charges': charges, 'account_id': account_id})


@login_required
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

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = Account.objects.create(user=request.user,
                                             number=form.cleaned_data['number'],
                                             name=form.cleaned_data['name'])
            account.save()
            return render(request, 'finish_charge.html')
    else:
        form = AccountForm()
    return render(request, 'add_from.html', {'form': form, 'path': '/add_account/'})
