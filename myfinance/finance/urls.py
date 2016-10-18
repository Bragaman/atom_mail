from django.conf.urls import url
from finance.views import *

urlpatterns = [
    url(r'^$', home_page),
    url(r'^charges/$', charges_page)
]