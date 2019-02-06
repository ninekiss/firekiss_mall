from django.conf.urls import url
from goods.views import Index, Detail, List
urlpatterns = [
    url(r'^index$', Index.as_view(), name='index'),
    url(r'^goods/(?P<goods_id>\d+)$', Detail.as_view(), name='detail'),
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', List.as_view(), name='list'),

]
