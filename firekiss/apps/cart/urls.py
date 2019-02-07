from django.conf.urls import url
from cart.views import CartShow, CartAdd, CartUpdate, CartDelete


urlpatterns = [
   url(r'^add$', CartAdd.as_view(), name='add'),  # 添加购物车记录
   url(r'^update$', CartUpdate.as_view(), name='update'),  # 更新购物车记录
   url(r'^delete$', CartDelete.as_view(), name='delete'),  # 删除购物车记录
   url(r'^$', CartShow.as_view(), name='show'),  # 显示购物车页面
]
