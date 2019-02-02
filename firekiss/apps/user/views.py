from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from celery_task.tasks import send_confirm_mail
from django.conf import settings
from user.models import User, Address
from goods.models import  GoodsSKU
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
from utils.fdfs.storage import FDFSStorage
from django_redis import get_redis_connection



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
        user = User.objects.create_user(username=username, password=password, email=mail, tel=tel)
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
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            remember = 'checked'
        else:
            username = ''
            remember = ''
        return render(request, 'login.html', {"username": username, "remember": remember})

    def post(self, request):
        """登录处理"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {"msg": "数据不完整,请重试"})
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # 用户已激活

                # 记录用户登录状态
                login(request, user)

                # 获取登录之前的url
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))

                # 登录成功之后跳转到登录之前的url
                response = redirect(next_url)

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名,cookie存活时间为7天
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {"msg": "账户未激活，请查收激活邮件进行激活"})

        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误,请重试"})


class Logout(View):
    def get(self, request):
        # 注销登录
        logout(request)
        # 跳转到首页
        return redirect(reverse('goods:index'))



class UserCenter(LoginRequiredMixin, View):
    """用户中心"""
    def get(self, request):
        """显示用户中心页面"""
        # request.user
        # 如果用户未登录，user为AnonymousUser类的实例对象，is_authenticated()返回值永远是False
        # 如果用已登录，user为User类的实例对象，is_authenticated()返回值永远是True
        # 除了自定义传递数据，django默认会把user对象也传递给模板

        # 获取用户历史浏览记录
        # 使用redis存储用户历史浏览记录，使用list
        # history_用户id 作为key， 浏览过的商品id作为value,从左边插入数据
        user = request.user
        # 连接redis
        con = get_redis_connection("default")
        history_key = 'history_%d' % user.id

        hist_ids = con.lrange(history_key, 0, 4)  # 获取最新的5条

        goods_list = []
        for hist_id in hist_ids:
            goods = GoodsSKU.objects.get(id=hist_id)
            goods_list.append(goods)

        # 组织模板上下文
        context = {
            "page": "user",
            "goods_list": goods_list
        }

        return render(request, 'base_user_center.html', context)

    def post(self, request):
        """用户修改个人资料"""
        # 接收收据(当前版本只支持修改头像)
        user = request.user
        avatar = request.FILES.get('avatar')
        # 校验数据
        if avatar is None:
            return redirect(reverse('user:user'))

        # 进行业务处理

        # 获取用户对象
        user = User.objects.get(id=user.id)

        if user:
            # 使用自定义存储类储存用户上传的文件
            storage = FDFSStorage()
            filename = storage.save(avatar.name, avatar)

            # 修改头像
            user.avatar = filename
            user.save()

        # 返回应答
        return redirect(reverse('user:user'))



class UserAddress(LoginRequiredMixin, View):
    # 获取用户默认收货地址
    def get(self, request):
        # 进行业务处理
        user = request.user
        address = Address.objects.get_default_addr(user)
        return render(request, 'user_address.html', {"page": "address", "address": address})

    def post(self, request):
        # 获取数据
        receiver = request.POST.get('receiver')
        phone = request.POST.get('phone')
        area = request.POST.get('area')
        addr = request.POST.get('addr')

        # 校验数据
        if not all([receiver, phone, area, addr]):
            return render(request, 'user_address.html', {"page": "address", "msg": "数据不完整"})
        if not re.match(r'^1[34578][0-9]{9}$', phone):
            return render(request, 'user_address.html', {"page": "address", "msg": "手机格式不正确"})

        # 进行业务处理
        user = request.user

        address = Address.objects.get_default_addr(user)

        if address:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user_id=user, receiver=receiver, phone=phone, area=area, addr=addr, is_default=is_default)
        # 返回应答
        return redirect(reverse('user:address'))


class UserOrder(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_order.html', {"page": "order"})


class PayMethod(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_build.html', {"page": "pay_method"})


class Safety(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_build.html', {"page": "safety"})


class Privacy(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_build.html', {"page": "privacy"})