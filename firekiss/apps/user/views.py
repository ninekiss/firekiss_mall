from django.shortcuts import render
from django.http import JsonResponse
from user.models import User
import re

# Create your views here.


# /user/register
def register(request):
    """用户注册"""
    return render(request, 'register.html')


# /user/register
def register_handle(request):
    """注册处理"""
    # 接收收据
    usr_name = request.GET.get('name')
    username = request.POST.get('name')
    password = request.POST.get('pwd')
    apassword = request.POST.get('apwd')
    tel = request.POST.get('tel')
    mail = request.POST.get('mail')
    ver_code = request.POST.get('code')

    # 校验数据

    # get 请求
    if request.method == 'GET':
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=usr_name)
        except User.DoesNotExist:
            # 数据库中该用户名不存在则抛出该异常
            user = None

        if user:
            # 用户名已存在(没抛异常)
            return JsonResponse({"msg": "existed"})

        print(username)

    # post 请求
    if request.method == 'POST':
        # 校验数据完整性
        if not all([username, password, apassword, tel, mail, ver_code]):
            return JsonResponse({"msg": "incomplete"})

        # 其他数据本版本后端不做校验
        # 校验邮箱
        ret = re.match(r'^[\-_]?[A-Za-z\d\.]+[\-_]?[A-Za-z\d\.]+[\-_]?@[\-_]?[A-Za-z\d]+[\-_]?[A-Za-z\d]+[\-_]?\.[A-Za-z]{2,6}(\.[A-Za-z]{2,6})*$', mail)
        if not ret:
            return JsonResponse({"msg": "email_illegal"})

        # 进行业务处理:注册用户
        user = User.objects.create(username=username, password=password, email=mail, tel=tel)
        user.is_active = 0
        user.save()

        # 返回应答
        return JsonResponse({"msg": "success"})
