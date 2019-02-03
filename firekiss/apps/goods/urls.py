from django.conf.urls import url
from goods.views import Index, Video
urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'video', Video.as_view(), name='video'),

]
