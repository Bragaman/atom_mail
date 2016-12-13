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
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/stats/', views.MonthStatCollection.as_view())
]