from django.conf.urls import url, include
from rest_framework import routers

from finance import views
from finance.views import *


router = routers.DefaultRouter()
router.register(r'accounts/?', views.AccountViewSet)
router.register(r'charges/?', views.ChargeViewSet)

urlpatterns = [
    url(r'^$', home_page),
    url(r'^charges/(\d+)/$', account_charges),
    url(r'^add_charge/(\d+)/$', add_account_charge, ),
    url(r'^add_account/$', add_account, ),
    url(r'^account/register/$', register_user, name='register_user'),

    url(r'^accounts/$', AccountList.as_view(), name='accounts_list'),
    url(r'^accounts/(?P<pk>\d+)/$', AccountDetail.as_view(), name='accounts_detail'),
    url(r'^accounts/(?P<pk>\d+)/edit/$', AccountUpdate.as_view(), name='accounts_update'),
    url(r'^accounts/(?P<pk>\d+)/delete/$', AccountDelete.as_view(), name='accounts_delete'),
    url(r'^accounts/create/$', AccountCreate.as_view(), name='accounts_create'),

    url(r'^accounts/(?P<account_id>\d+)/charge/create/$', ChargeCreate.as_view(), name='charge_create'),
    url(r'^accounts/(?P<account_id>\d+)/charge/(?P<pk>\d+)/edit/$', ChargeUpdate.as_view(), name='charge_update'),
    url(r'^accounts/(?P<account_id>\d+)/charge/(?P<pk>\d+)/delete/$', ChargeDelete.as_view(), name='charge_delete'),

    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/stats/', views.MonthStatCollection.as_view())
]