from django.conf.urls import url
from finance.views import *

urlpatterns = [
    url(r'^$', home_page),
    url(r'^charges/(\d+)/$', account_charges),
    url(r'^add_charge/(\d+)/$', add_account_charge, ),
    url(r'^add_account/$', add_account, ),
    url(r'^login/$', login),
    url(r'logout/$', logout),
]