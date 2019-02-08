from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from goods.models import GoodsSKU
from user.models import Address
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin

# Create your views here.

class OrderPlace(LoginRequiredMixin, View):
    """订单提交页面"""
    # def get(self, request):
    #     return redirect(reverse('goods:index'))

    def post(self, request):

        user = request.user

        # 接收数据
        # 商品id(详情页的直接请求为1个，购物车页面请求可能为多个)
        sku_ids = request.POST.getlist('sku_ids')

        # 商品数量(只有详情页的请求才会有)
        count = request.POST.get('count')

        # 校验数据
        # 校验数据完整性
        if not sku_ids:
            return redirect(reverse('cart:show'))
        # 校验数量
        if count:
            request_count = int(count)
        else:
            request_count = 0

        # 进行业务处理
        con = get_redis_connection('default')
        cart_key = 'cart_user%d' % user.id

        # 商品总计金额和数量
        total_count = 0
        total_price = 0

        sku_list = list()
        # 遍历sku_ids
        for sku_id in sku_ids:
            # 校验商品是否存在
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                return redirect(render('cart:show'))
            # 获取用户购物车中的商品数量
            count = con.hget(cart_key, sku_id)
            if count:
                count = int(count)

            if request_count != 0:
                # 请求时携带count,则是详情页过来的请求
                count = request_count
                # 返回给页面用来处理订单
                res_count = count
            else:
                res_count = 0

            # 商品小计
            amount = sku.real_price * count

            # 商品优惠(模拟优惠0元)
            pref = 1

            # sku动态增加属性
            sku.count = count
            sku.amount = amount-pref
            sku.pref = pref

            # 商品总计金额和数量
            total_count += count
            total_price += sku.amount
            # 订单商品列表
            sku_list.append(sku)

        # 运费(模拟运费0元)
        tran_price = 0

        # 火吻优惠(模拟优惠0元)
        pref = 2

        # 实付金额
        total_pay = total_price - pref - tran_price

        # 获取用户收货地址
        addr_list = Address.objects.filter(user_id=user)

        # sku_ids
        sku_ids = ','.join(sku_ids)

        # 组织模板上下文
        context = {
            "sku_list": sku_list,
            "tran_price": tran_price,
            "pref": pref,
            "total_count": total_count,
            "total_price": total_price,
            "total_pay": total_pay,
            "addr_list": addr_list,
            "sku_ids": sku_ids,
            "res_count": res_count
        }

        # 返回应答
        return render(request, 'order_place.html', context)
