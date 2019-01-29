from django.db import models
from db.base_model import BaseModel


# Create your models here.
class OrderInfo(BaseModel):
    """订单信息模型类"""
    PAY_METHOD_CHOICES = (
        (0, 'kisspay'),
        (1, '信用卡'),
        (2, '银联支付'),
        (3, '支付宝'),
        (4, '微信支付'),
        (5, 'paypal'),
        (6, '货到付款'),
        (7, '比特币')

    )

    ORDER_STATUS_CHOICES = (
        (0, '已取消'),
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单编号')
    user = models.ForeignKey('user.User', verbose_name='用户')
    addr = models.ForeignKey('user.Address', verbose_name='地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, verbose_name='支付方式')
    total_count = models.IntegerField(default=1, verbose_name='数目')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='优惠金额')
    real_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实付金额')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, verbose_name='订单状态')
    pay_id = track_id = models.CharField(max_length=128, unique=True, verbose_name='支付编号')
    track_id = models.CharField(max_length=128, unique=True, verbose_name='物流编号')

    class Meta:
        db_table = 'fk_order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """订单商品模型类"""
    order = models.ForeignKey('OrderInfo', verbose_name='订单')
    sku = models.ForeignKey('goods.GoodsSKU', verbose_name='商品SKU')
    count = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')

    class Meta:
        db_table = 'fk_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


class GoodsAppraisal(BaseModel):
    """商品评价模型类"""
    APPR_STATUS = (
        (0, '默认评价'),
        (1, '初次评价'),
        (2, '追加评价'),
        (3, '掌柜解释'),
    )
    goods = models.ForeignKey('OrderGoods', verbose_name='评价商品')
    user = models.ForeignKey('user.User', verbose_name='评价用户')
    appr_status = models.SmallIntegerField(choices=APPR_STATUS, verbose_name='评论分类')
    detail_star = models.SmallIntegerField(default=0, verbose_name='描述星评')
    saler_star = models.SmallIntegerField(default=0, verbose_name='卖家星评')
    track_star = models.SmallIntegerField(default=0, verbose_name='物流星评')
    about_goods = models.CharField(max_length=1000, verbose_name='对商品评价')
    about_server = models.CharField(max_length=1000, verbose_name='对服务评价')

    class Meta:
        db_table = 'fk_goods_appraisal'
        verbose_name = '商品评价'
        verbose_name_plural = verbose_name


class AppraisalImage(BaseModel):
    """评价图片模型类"""
    appr = models.ForeignKey('GoodsAppraisal', verbose_name='评价')
    image = models.ImageField(upload_to='appraisal_image', verbose_name='评价图片')

    class Meta:
        db_table = 'fk_appraisal_image'
        verbose_name = '评价图片'
        verbose_name_plural = verbose_name