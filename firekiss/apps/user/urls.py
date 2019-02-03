from django.conf.urls import url
from user.views import Register, Active, Login, Logout, UserCenter, UserAddress, UserOrder, PayMethod, Safety, Privacy 


urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    url(r'^register$', Register.as_view(), name='register'),  # 注册类视图
    url(r'^active/(?P<token>.*)$', Active.as_view(), name='active'),  # 激活类视图
    url(r'^login$', Login.as_view(), name='login'),  # 登录类视图
    url(r'^logout$', Logout.as_view(), name='logout'),  # 注销登录

    # 用户中心
    url(r'^$', UserCenter.as_view(), name='user'),  # 默认显示个人资料
    url(r'^address$', UserAddress.as_view(), name='address'),  # 收货地址
    url(r'^order$', UserOrder.as_view(), name='order'),  # 我的订单
    url(r'^pay_method$', PayMethod.as_view(), name='pay_method'),  # 支付设置
    url(r'^safety$', Safety.as_view(), name='safety'),  # 安全设置
    url(r'^privacy$', Privacy.as_view(), name='privacy'),  # 隐私设置


]
