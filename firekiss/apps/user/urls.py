from django.conf.urls import url
from user.views import Register, Active, Login


urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    url(r'^register$', Register.as_view(), name='register'),  # 注册类视图
    url(r'^active/(?P<token>.*)$', Active.as_view(), name='active'),  # 激活类视图
    url(r'^login$', Login.as_view(), name='login'),  # 登录类视图

]
