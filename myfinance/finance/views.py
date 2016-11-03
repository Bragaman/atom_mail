from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from finance.forms import *


def home_page(request):
    return render(request, 'home_page.html')


def charges_page(request):
    return render(request, 'charges_page.html')


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
