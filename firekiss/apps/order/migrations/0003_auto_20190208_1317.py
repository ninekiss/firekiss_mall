# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190130_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsappraisal',
            name='about_goods',
            field=models.CharField(verbose_name='对商品评价', max_length=1000, default='未作出评价,系统默认好评!'),
        ),
        migrations.AlterField(
            model_name='goodsappraisal',
            name='appr_status',
            field=models.SmallIntegerField(verbose_name='评论分类', choices=[(0, '默认评价'), (1, '初次评价'), (2, '追加评价'), (3, '初评解释'), (4, '追评解释')]),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_status',
            field=models.SmallIntegerField(verbose_name='订单状态', default=1, choices=[(0, '已取消'), (1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')]),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_id',
            field=models.CharField(verbose_name='支付编号', max_length=128, default=''),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='track_id',
            field=models.CharField(verbose_name='物流编号', max_length=128, default=''),
        ),
    ]
