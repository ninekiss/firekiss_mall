from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse

from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin


class CartShow(LoginRequiredMixin, View):
    """购物车页面"""
    def get(self, request):
        # 业务处理:展示登录用户购物车中的商品

        # 获取用户
        user = request.user

        # 获取用户购物车中的商品数据
        con = get_redis_connection('default')
        # 组织key
        cart_key = 'cart_user%d' % user.id
        # 获取商品id及数量的字典,key不存在返回None
        cart_dict = con.hgetall(cart_key)

        sku_list = []

        total_count = 0

        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            # 给sku动态添加count属性，用来保存商品数量
            sku.count = count
            # 小计
            sku.amount = sku.real_price*int(count)
            # 购物车中商品总数量
            total_count += int(count)
            sku_list.append(sku)

        # 组织模板上下文
        content = {
            'sku_list': sku_list,
            'total_count': total_count
        }

        return render(request, 'goods_cart.html', content)


class CartAdd(View):
    """添加商品到购物车"""
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收数据

        # 商品id(sku_id)
        sku_id = request.POST.get('sku_id')
        # 添加的数量(count)
        count = request.POST.get('count')

        # 校验数据

        # 校验完整性
        if not all([sku_id, count]):
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验数量是否合法
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({"status": 202, "msg": "数量不合法"})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"status": 203, "msg": "商品不存在"})

        # 进行业务处理:向购物车中添加商品
        con = get_redis_connection('default')
        # 组织key
        cart_key = 'cart_user%d' % user.id
        # 尝试获取key对应的field的值(购物车中对应商品的数量)
        cart_count = con.hget(cart_key, sku_id)
        # 如果不存在则返回None
        if cart_count:
            count += int(cart_count)

        # 校验添加后的总数量是否超过库存
        if count > sku.stock:
            return JsonResponse({"status": 204, "msg": "库存不足"})

        # 向购物车中添加商品或更新已存在的商品数量
        con.hset(cart_key, sku_id, count)

        # 获取购物车中的商品数目
        total = con.hlen(cart_key)

        # 返回应答
        return JsonResponse({"status": 200, "msg": "添加成功", "total": total})



class CartUpdate(View):
    """更新购物车中的商品记录"""
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收数据

        # 商品id(sku_id)
        sku_id = request.POST.get('sku_id')
        # 添加的数量(count)
        count = request.POST.get('count')

        # 校验数据

        # 校验完整性
        if not all([sku_id, count]):
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验数量是否合法
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({"status": 202, "msg": "数量不合法"})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"status": 203, "msg": "商品不存在"})

        # 进行业务处理:更新购物车中的商品记录
        con = get_redis_connection('default')
        # 组织key
        cart_key = 'cart_user%d' % user.id

        # 校验添加后的总数量是否超过库存
        if count > sku.stock:
            return JsonResponse({"status": 204, "msg": "库存不足"})

        # 向购物车中添加商品或更新已存在的商品数量
        con.hset(cart_key, sku_id, count)

        # 获取购物车中的商品数量
        total = 0

        vals = con.hvals(cart_key)

        if vals:
            for val in vals:
                total += int(val)

        # 返回应答
        return JsonResponse({"status": 200, "msg": "更新成功", "total": total})


class CartDelete(View):
    """购物车记录删除"""
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收参数
        # 商品id(sku_id)
        sku_id = request.POST.get('sku_id')

        print(sku_id)

        # 校验完整性
        if not sku_id:
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"status": 203, "msg": "商品不存在"})

        # 进行业务处理:删除购物车中的商品
        con = get_redis_connection('default')
        # 组织key
        cart_key = 'cart_user%d' % user.id

        # 删除
        con.hdel(cart_key, sku_id)

        # 获取购物车中的商品数量
        total = 0

        vals = con.hvals(cart_key)

        if vals:
            for val in vals:
                total += int(val)

        # 返回应答
        return JsonResponse({"status": 200, "msg": "删除成功", "total": total})