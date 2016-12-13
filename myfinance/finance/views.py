from django.shortcuts import render, redirect
from rest_framework import views as rest_views
from rest_framework import viewsets
from rest_framework.response import Response

from finance.forms import *
from django.contrib.auth.decorators import login_required
from finance.serializers import *


@login_required
def home_page(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'home_page.html', {'accounts':accounts})


@login_required
def account_charges(request, account_id):
    # TODO check user
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


def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(**user_form.cleaned_data)
            profile_cleaned = profile_form.cleaned_data
            user.profile.phone_number = profile_cleaned['phone_number']
            user.profile.address = profile_cleaned['address']
            user.save()
            return redirect('/')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# API
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer


class MonthStatCollection(rest_views.APIView):
    DUMMY_VALUES = [
        {'month': 'december', 'amount': -1000.90},
        {'month': 'november', 'amount': 530.00},
    ]

    def get(self, request, format=None):
        serializer = MonthStatSerializer(self.DUMMY_VALUES, many=True)
        return Response(serializer.data)