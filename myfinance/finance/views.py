from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from rest_framework import views as rest_views
from rest_framework import viewsets
from rest_framework.response import Response

import csv
from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from finance.serializers import *
from finance.forms import *
from finance.mixins import SuperUserRequiredMixin
from finance.utils import *


# @login_required
def home_page(request):
    return render(request, 'home_page.html')


def register_user(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            # user = User.objects.create(**form.cleaned_data)
            profile_cleaned = profile_form.cleaned_data
            user.profile.phone_number = profile_cleaned['phone_number']
            user.profile.address = profile_cleaned['address']
            user.save()
            return redirect('/')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'profile_form.html', {
        'user_form': form,
        'profile_form': profile_form
    })


# Accounts
class AccountList(LoginRequiredMixin, ListView):
    template_name = 'account/list.html'

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)


class AccountDetail(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and obj.user != user:
            raise PermissionDenied()
        return obj


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and obj.user != user:
            raise PermissionDenied()
        return obj

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('accounts_list'))


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'account/delete.html'
    success_url = '/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and obj.user != user:
            raise PermissionDenied()
        return obj


@login_required
def account_stats(request, *args, **kwargs):
    pk = kwargs.get("pk")
    account_queryset = Account.objects.filter(id=pk)
    if account_queryset:
        account = check_account_owner(account_queryset, request)
        stats = account.get_account_stats()
        return render(request,
                      'account/statistic.html',
                      {'stats': stats,
                       'pk': pk}
                      )
    return HttpResponseNotFound()


@login_required
def account_report(request, *args, **kwargs):
    account_queryset = Account.objects.filter(id=kwargs.get("pk"))
    if account_queryset:
        account = check_account_owner(account_queryset, request)
        stats = account.get_account_stats()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Amount'])
        for i in stats:
            writer.writerow([i['month'], i['amount']])

        return response
    return HttpResponseNotFound()


# Charges
class ChargeCreate(LoginRequiredMixin, CreateView):
    model = Charge
    form_class = ChargeForm
    template_name = 'charge/form.html'

    def form_valid(self, form):
        account = Account.objects.filter(id=self.kwargs["account_id"])
        user = self.request.user
        if not user.is_superuser and account[0].user != user:
            raise PermissionDenied()
        if account:
            instance = form.save(commit=False)
            instance.account = account[0]
            instance.save()
            return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))
        raise PermissionDenied()


class ChargeUpdate(LoginRequiredMixin, UpdateView):
    model = Charge
    fields = ['value', 'date']
    template_name = 'charge/form.html'

    def form_valid(self, form):
        account = Account.objects.filter(id=self.kwargs["account_id"])
        user = self.request.user
        if not user.is_superuser and account[0].user != user:
            raise PermissionDenied()
        if account:
            instance = form.save(commit=False)
            instance.account = account[0]
            instance.save()
            return redirect(reverse_lazy('accounts_detail', kwargs={'pk': account[0].id}))
        raise PermissionDenied()


class ChargeDelete(LoginRequiredMixin, DeleteView):
    model = Charge
    template_name = 'charge/delete.html'
    success_url = '/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and obj.account.user != user:
            raise PermissionDenied()
        return obj


# User profile
class UserProfileList(SuperUserRequiredMixin, ListView):
    template_name = 'profile/list.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return super().handle_no_permission()


class UserProfileDetail(SuperUserRequiredMixin, DetailView):
    model = User
    template_name = 'profile/detail.html'


class UserProfileCreate(SuperUserRequiredMixin, CreateView):
    model = User
    form_class = ProfileCreateForm
    template_name = 'profile/form.html'

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('accounts_list'))


class UserProfileUpdate(SuperUserRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile/form.html'
    success_url = '/'

    def get_initial(self):
        res = super().get_initial()
        user = self.get_object()
        res['phone_number'] = user.profile.phone_number
        res['address'] = user.profile.address
        return res

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class UserProfileDelete(SuperUserRequiredMixin, DeleteView):
    model = User
    template_name = 'account/delete.html'
    success_url = '/'


# ------------------------------------------------------API-----------------------------------------------------
class AccountViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset_by_username(self, request):
        if "username" in self.request.query_params:
            username = self.request.query_params.get("username", None)
            user_queryset = User.objects.filter(username=username)
            if user_queryset:
                self.queryset = Account.objects.filter(user=user_queryset[0].id)
            else:
                return False
        else:
            self.queryset = Account.objects.filter(user=request.user.id)
        return True

    def list(self, request, *args, **kwargs):
        if self.get_queryset_by_username(request):
            return super().list(request, *args, **kwargs)
        return HttpResponseNotFound('No user with this name')

    def create(self, request, *args, **kwargs):
        if self.get_queryset_by_username(request):
            return super().create(request, *args, **kwargs)
        return HttpResponseNotFound('No user with this name')


class ChargeViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer

    def list(self, request, *args, **kwargs):
        if "account_number" in self.request.query_params:
            account_queryset = Account.objects.filter(number=self.request.query_params.get("account_number", None))
            if account_queryset:
                check_account_owner(account_queryset, request)
                self.queryset = Charge.objects.filter(account=account_queryset[0].id)
                return super().list(request, *args, **kwargs)
            return HttpResponseNotFound('No account with this number')

        return HttpResponseNotFound('Only with number account here')


class UserProfileViewSet(SuperUserRequiredMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if "username" in self.request.query_params:
            return User.objects.filter(username=self.request.query_params.get("username", None))
        else:
            return User.objects.filter(username=self.request.user.username)

    def create(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only GET here')

    def destroy(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only GET here')


class MonthStatCollection(LoginRequiredMixin, rest_views.APIView):
    def get(self, request, format=None):
        if "account_number" in self.request.query_params:
            account_queryset = Account.objects.filter(number=self.request.query_params.get("account_number", None))
            if account_queryset:
                account = check_account_owner(account_queryset, request)
                stats = account.get_account_stats()
                serializer = MonthStatSerializer(stats, many=True)
                return Response(serializer.data)
            return HttpResponseNotFound("Wrong query arg")
        return HttpResponseNotFound("Wrong query arg 'account_number' is required")