from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.db import transaction
from django.conf import settings

from goods.models import GoodsSKU
from user.models import Address
from order.models import OrderInfo, OrderGoods
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from datetime import datetime
from alipay import AliPay
import os
import time

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
            pref = 0

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
        pref = 0

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


class OrderCommit(View):
    """订单提交请求"""
    # 开启一个mysql事务(transaction.atomic()对视图进行装饰)
    @transaction.atomic
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收数据
        # 地址
        addr_id = request.POST.get('addr_id')
        # 商品sku_ids
        sku_ids = request.POST.get('sku_ids')
        # 商品数量
        req_count = request.POST.get('req_count')
        # 模拟支付方式(支付宝)
        pay_method = '3'

        # 校验数据
        # 校验完整性
        if not all([addr_id, sku_ids, req_count, pay_method]):
            # 数据不完整
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id, user_id=user)
        except Address.DoesNotExist:
            return JsonResponse({"status": 202, "msg": "地址不存在"})

        # 校验数量
        try:
            req_count = int(req_count)
        except Exception as e:
            return JsonResponse({"status": 203, "msg": "数量不合法"})

        # 校验支付方式
        res = OrderInfo.PAY_METHOD.get(pay_method)
        if not res:
            return JsonResponse({"status": 204, "msg": "支付方式不支持"})

        # todo: 进行业务处理: 1.添加订单到订单表

        # 总数
        total_count = 0
        # 总价
        total_price = 0
        # 订单编号 2019021516223501001
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '0%d001' % user.id
        # 模拟运费
        transit_price = 0
        # 模拟优惠金额
        promo_price = 0
        # 实付金额
        real_paid = 0

        # 设置事务保存点,返回事务保存点id
        save_id = transaction.savepoint()

        try:
            # todo: 向订单表中插入一条记录
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price,
                promo_price=promo_price,
                real_paid=real_paid,
            )

            # todo: 进行业务处理: 2.添加订单商品到订商品表
            # 把sku_ids字符串变成列表
            sku_ids = sku_ids.split(',')

            # 获取用户购物车商品数量
            con = get_redis_connection('default')
            # 组织key
            cart_key = 'cart_user%d' % user.id

            # 遍历sku_ids
            for sku_id in sku_ids:
                # 乐观锁更新失败多尝试三次
                for i in range(3):
                    # 校验sku
                    try:
                        # todo: 悲观锁，查询时别人不能查
                        #   相当于 select * from fk_goods_sku where id=sku_id for update;
                        # sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except GoodsSKU.DoesNotExist:
                        # 出错时，回滚事务
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({"status": 205, "msg": "商品不存在"})

                    # todo:如果订单来自详情页直接购买，则数量不为0
                    #   如果订单请求来自购物车，则请求数量为0，需要从购物车获取
                    count = con.hget(cart_key, sku_id)

                    if req_count != 0:
                        # 请求来详情页
                        count = req_count

                    # 数量
                    count = int(count)

                    # todo:判断库存
                    if count > sku.stock:
                        # 出错时，回滚事务
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({"status": 206, "msg": "库存不足"})

                    # todo: 乐观锁，查询时不上锁，更新时判断与原来的数据不相同相同，则更新失败
                    #   相当于 update fk_goods_sku set stock=new_stock, sales=new_sales
                    #   where id=sku_id and stock=origin_stock

                    # 原始库存
                    origin_stock = sku.stock
                    # 原始销量
                    origin_sales = sku.sales
                    # 更新商品库存
                    new_stock = origin_stock - count
                    # 更新商品销量
                    new_sales = origin_sales + count

                    # 返回受影响的行数(1或0)
                    res = GoodsSKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0:
                        if i == 2:
                            # 尝试第三次依旧失败
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({"status": 306, "msg": "订单出错"})
                        # 不到三次，继续尝试
                        continue
                    # 更新成功，跳出循环
                    break
                # 更新商品库存
                # sku.stock -= count
                # 更新商品销量
                # sku.sales += count

                # sku.save()

                # 商品小计
                amount = sku.real_price*count


                # todo: 向订单商品表中插入一条记录
                order_sku = OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=amount
                )

                # 更新总价和总数量
                total_price += amount
                total_count += count

            # 实付金额
            real_paid = total_price - transit_price - promo_price

            # 更新订单数据
            order.total_count = total_count
            order.total_price = total_price
            order.real_paid = real_paid
            order.save()
        except Exception as e:
            # 出错时，回滚事务
            print(e)
            transaction.savepoint_rollback(save_id)
            return JsonResponse({"status": 207, "msg": "订单创建失败"})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # todo: 清除用户购物车中对应的记录
        con.hdel(cart_key, *sku_ids)

        # 返回应答
        return JsonResponse({"status": 200, "msg": "订单创建成功", "order_id": order_id})


class OrderPay(View):
    """订单支付"""
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收数据
        order_id = request.POST.get('order_id')

        # 校验数据
        # 校验数据完整性
        if not order_id:
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验订单
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({"status": 202, "msg": "订单错误"})

        # 进行业务处理:调用支付宝
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_dev_public_key.pem')).read()
        print(app_private_key_string)
        print(alipay_public_key_string)
        alipay = AliPay(
            appid="2016092400583881",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=True  # 默认False,(True为沙箱)
        )

        # 调用支付接口
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.real_paid),  # Decimal不能被序列化
            subject='火吻订单支付:%s' % order_id,
            return_url=None,
            notify_url=None
        )
        # 支付url
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        # 返回应答
        return JsonResponse({"status": 200, "msg": "支付环境已准备", "pay_url": pay_url})


class OrderCheck(View):
    """支付状态查询"""
    def post(self, request):
        user = request.user
        # 判断用户是否登录
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({"status": 301, "msg": "用户未登录"})

        # 接收数据
        order_id = request.POST.get('order_id')

        # 校验数据
        # 校验数据完整性
        if not order_id:
            return JsonResponse({"status": 201, "msg": "数据不完整"})

        # 校验订单
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({"status": 202, "msg": "订单错误"})

        # 进行业务处理: 进行订单支付交易状态查询
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_dev_public_key.pem')).read()
        print(app_private_key_string)
        print(alipay_public_key_string)
        alipay = AliPay(
            appid="2016092400583881",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=True  # 默认False,(True为沙箱)
        )

        # 调用支付宝交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(out_trade_no=order_id)

            # 状态码
            code = response.get('code')
            # 交易状态
            trade_status = response.get('trade_status')

            if code == '10000' and trade_status == 'TRADE_SUCCESS':
                # 交易成功
                trade_no = response.get('trade_no')

                # 更行订单状态(模拟跳到待评价:4)
                order.order_status = 4
                # 支付交易号
                order.pay_id = trade_no
                order.save()
                # 返回应答
                return JsonResponse({"status": 200, "msg": "支付成功"})
            elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
                # 等待付款
                # 业务处理失败，等待几秒待用户付款后再次查询
                time.sleep(5)
                # 再次查询
                continue
            else:
                # 交易失败
                return JsonResponse({"status": 203, "msg": "支付失败"})