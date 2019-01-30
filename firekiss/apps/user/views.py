from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from celery_task.tasks import send_confirm_mail
from django.conf import settings
from user.models import User

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re


# Create your views here.

# 使用类视图
class Register(View):
    """注册"""

    def get(self, request):
        """get 请求"""
        usr_name = request.GET.get('name')
        if not usr_name:
            # 显示注册页面
            return render(request, 'register.html')
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=usr_name)
        except User.DoesNotExist:
            # 数据库中该用户名不存在则抛出该异常
            user = None
        if user:
            # 用户名已存在(没抛异常)
            return JsonResponse({"msg": "existed"})
        return JsonResponse({"msg": "no_repeat"})


    def post(self, request):
        """post 请求"""
        # 接收收据
        username = request.POST.get('name')
        password = request.POST.get('pwd')
        apassword = request.POST.get('apwd')
        tel = request.POST.get('tel')
        mail = request.POST.get('mail')
        ver_code = request.POST.get('code')

        # 校验数据完整性
        if not all([username, password, apassword, tel, mail, ver_code]):
            return JsonResponse({"msg": "incomplete"})

        # 其他数据本版本后端不做校验
        # 校验邮箱
        ret = re.match(
            r'^[\-_]?[A-Za-z\d\.]+[\-_]?[A-Za-z\d\.]+[\-_]?@[\-_]?[A-Za-z\d]+[\-_]?[A-Za-z\d]+[\-_]?\.[A-Za-z]{2,6}(\.[A-Za-z]{2,6})*$',
            mail)
        if not ret:
            return JsonResponse({"msg": "email_illegal"})
        user = User.objects.create(username=username, password=password, email=mail, tel=tel)
        user.is_active = 0
        user.save()

        # 发送激活邮件到用户邮箱
        # 激活链接 http://192.168.0.100:8000/user/active/id
        # 激活链接要包含用户信息

        # 对用户信息进行加密(使用itsdangerous)
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 发送邮件
        send_confirm_mail.delay(mail, user.username, token)

        return JsonResponse({"msg": "success"})


class Active(View):
    """用户激活"""
    def get(self, request, token):

        # 进行解密， 获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 激活用户的id
            user_id = info['confirm']
            print(user_id)
            # 激活用户
            user = User.objects.get(id=user_id)
            print(user)
            user.is_active = 1
            user.save()

            # 使用反向解析重定向到登录页
            return redirect(reverse('user:login'))
        except SignatureExpired:
            # 激活链接已失效
            return HttpResponse('激活链接已失效')

class Login(View):
    """登录"""
    def get(self, request):
        """显示登陆页面"""
        return render(request, 'login.html')