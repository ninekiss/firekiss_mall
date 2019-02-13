from django.conf.urls import url
from order.views import OrderPlace, OrderCommit, OrderPay, OrderCheck


urlpatterns = [
    url(r'^place$', OrderPlace.as_view(), name='place'),
    url(r'^commit$', OrderCommit.as_view(), name='commit'),
    url(r'^pay$', OrderPay.as_view(), name='pay'),
    url(r'^check$', OrderCheck.as_view(), name='check'),
]
