# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppraisalImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('image', models.ImageField(verbose_name='评价图片', upload_to='appraisal_image')),
            ],
            options={
                'verbose_name': '评价图片',
                'verbose_name_plural': '评价图片',
                'db_table': 'fk_appraisal_image',
            },
        ),
        migrations.CreateModel(
            name='GoodsAppraisal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('appr_status', models.SmallIntegerField(verbose_name='评论分类', choices=[(0, '默认评价'), (1, '初次评价'), (2, '追加评价'), (3, '掌柜解释')])),
                ('detail_star', models.SmallIntegerField(verbose_name='描述星评', default=0)),
                ('saler_star', models.SmallIntegerField(verbose_name='卖家星评', default=0)),
                ('track_star', models.SmallIntegerField(verbose_name='物流星评', default=0)),
                ('about_goods', models.CharField(verbose_name='对商品评价', max_length=1000)),
                ('about_server', models.CharField(verbose_name='对服务评价', max_length=1000)),
            ],
            options={
                'verbose_name': '商品评价',
                'verbose_name_plural': '商品评价',
                'db_table': 'fk_goods_appraisal',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('count', models.IntegerField(verbose_name='数量', default=1)),
                ('price', models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'fk_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('order_id', models.CharField(verbose_name='订单编号', primary_key=True, max_length=128, serialize=False)),
                ('pay_method', models.SmallIntegerField(verbose_name='支付方式', choices=[(0, 'kisspay'), (1, '信用卡'), (2, '银联支付'), (3, '支付宝'), (4, '微信支付'), (5, 'paypal'), (6, '货到付款'), (7, '比特币')])),
                ('total_count', models.IntegerField(verbose_name='数目', default=1)),
                ('total_price', models.DecimalField(verbose_name='总金额', max_digits=10, decimal_places=2)),
                ('transit_price', models.DecimalField(verbose_name='运费', max_digits=10, decimal_places=2)),
                ('promo_price', models.DecimalField(verbose_name='优惠金额', max_digits=10, decimal_places=2)),
                ('real_paid', models.DecimalField(verbose_name='实付金额', max_digits=10, decimal_places=2)),
                ('order_status', models.SmallIntegerField(verbose_name='订单状态', choices=[(0, '已取消'), (1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')])),
                ('pay_id', models.CharField(verbose_name='支付编号', max_length=128, unique=True)),
                ('track_id', models.CharField(verbose_name='物流编号', max_length=128, unique=True)),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'fk_order_info',
            },
        ),
    ]
