# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190203_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockgoodstype',
            name='en_name',
            field=models.CharField(verbose_name='首页区域分类名英文', max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='blockgoodstype',
            name='image',
            field=models.ImageField(verbose_name='分类图片', blank=True, upload_to='block_goods_type'),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='bid_price',
            field=models.DecimalField(verbose_name='原价', blank=True, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='brand',
            field=models.ForeignKey(verbose_name='商品品牌', blank=True, to='goods.GoodsBrand'),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='comments',
            field=models.IntegerField(verbose_name='评价', blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='desc',
            field=models.CharField(verbose_name='简介', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='integral',
            field=models.IntegerField(verbose_name='积分', blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='sales',
            field=models.IntegerField(verbose_name='销量', blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='stock',
            field=models.IntegerField(verbose_name='库存', blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(verbose_name='商品种类', blank=True, to='goods.GoodsType'),
        ),
        migrations.AlterField(
            model_name='indexbrand',
            name='url',
            field=models.CharField(verbose_name='品牌链接', max_length=256, blank=True),
        ),
    ]
