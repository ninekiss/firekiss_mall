from django.conf.urls import url
from goods.views import Index, Detail
urlpatterns = [
    url(r'^index$', Index.as_view(), name='index'),
    url(r'^goods/(?P<goods_id>\d+)$', Detail.as_view(), name='detail'),
]
