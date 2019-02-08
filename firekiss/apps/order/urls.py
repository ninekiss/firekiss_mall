from django.conf.urls import url
from order.views import OrderPlace


urlpatterns = [
   url(r'^place$', OrderPlace.as_view(), name='place'),
]
