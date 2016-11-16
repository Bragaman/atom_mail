from django.conf.urls import url
from finance.views import *

urlpatterns = [
    url(r'^$', home_page),
    url(r'^fake_charges/$', charges_page),
    url(r'^charges/(\d+)/$', account_charges),
    url(r'^add_charge_no_model/$', add_charge_no_model, ),
    url(r'^add_charge/$', add_charge, ),
    url(r'^add_charge/(\d+)/$', add_account_charge, ),
    url(r'^add_account/$', add_account, ),
]