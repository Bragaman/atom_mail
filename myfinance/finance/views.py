from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from rest_framework import views as rest_views
from rest_framework import viewsets
from rest_framework.response import Response

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from finance.forms import *
from django.contrib.auth.decorators import login_required
from finance.serializers import *


@login_required
def home_page(request):
    return render(request, 'home_page.html')


@login_required
def account_charges(request, account_id):
    # TODO check user
    account = Account.objects.filter(id=account_id, user=request.user)
    if account:
        charges = Charge.objects.filter(account=account_id)
        return render(request, 'charges_page.html', {'charges': charges, 'account_id': account_id})
    else:
        return render(request, 'no_page.html', status=404)


@login_required
def add_account_charge(request, account_id):
    account = Account.objects.filter(id=account_id, user=request.user)
    if account:
        if request.method == "POST":
            form = ChargeForm(request.POST)
            if form.is_valid():
                new_charge = Charge.objects.create(account_id=account_id,
                                                   **form.cleaned_data)
                new_charge.save()
                return render(request, 'finish_charge.html')
        else:
            form = ChargeForm()
        return render(request, 'add_from.html', {'form': form,
                                                 'path': '/add_charge/{}/'.format(account_id)
                                                 })
    else:
        return render(request, 'no_page.html', status=404)


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


# Accounts
class AccountList(LoginRequiredMixin, ListView):
    template_name = 'account/list.html'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDetail(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/detail.html'


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'number']
    template_name = 'account/form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        # TODO ask why so
        return redirect(reverse_lazy('accounts_list'))


class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'number']
    template_name = 'account/form.html'
    success_url = '/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.get_success_url())


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'account/delete.html'
    success_url = '/'


# Charges
class ChargeCreate(LoginRequiredMixin, CreateView):
    model = Charge
    fields = ['value', 'date']
    template_name = 'charge/form.html'

    def form_valid(self, form):
        account = Account.objects.filter(id=self.kwargs["account_id"],
                                         user=self.request.user)
        if account:
            instance = form.save(commit=False)
            instance.account = account[0]
            instance.save()
            return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))
        # TODO go to error page
        return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))


class ChargeUpdate(LoginRequiredMixin, UpdateView):
    model = Charge
    fields = ['value', 'date']
    template_name = 'charge/form.html'

    def form_valid(self, form):
        account = Account.objects.filter(id=self.kwargs["account_id"],
                                         user=self.request.user)
        if account:
            instance = form.save(commit=False)
            instance.account = account[0]
            instance.save()
            return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))
        # TODO go to error page
        return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))


class ChargeDelete(LoginRequiredMixin, DeleteView):
    model = Charge
    template_name = 'charge/delete.html'
    success_url = '/'


# API
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer


class MonthStatCollection(rest_views.APIView):
    def get(self, request, format=None):
        values = dict()
        for account in Account.objects.filter(user=request.user):
            for charge in Charge.objects.filter(account=account):
                m = charge.date.strftime('%B%Y')
                if m in values:
                    values[m] += charge.value
                else:
                    values[m] = charge.value

        stats = list()
        for i, v in values.items():
            stats.append({'month': i, 'amount': v})
        serializer = MonthStatSerializer(stats, many=True)
        return Response(serializer.data)
