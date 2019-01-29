# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='商品SPU名称', max_length=128)),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'fk_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsBrand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('brand', models.CharField(verbose_name='品牌', max_length=64)),
                ('logo', models.ImageField(verbose_name='品牌logo', null=True, upload_to='goods_brand')),
            ],
            options={
                'verbose_name': '商品品牌',
                'verbose_name_plural': '商品品牌',
                'db_table': 'fk_goods_brand',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('image', models.ImageField(verbose_name='商品图片', upload_to='goods_image')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'fk_goods_image',
            },
        ),
        migrations.CreateModel(
            name='GoodsPromiseMapp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('is_support', models.BooleanField(verbose_name='是否支持', default=True)),
            ],
            options={
                'verbose_name': '商品服务承诺映射',
                'verbose_name_plural': '商品服务承诺映射',
                'db_table': 'fk_goods_promise_mapp',
            },
        ),
        migrations.CreateModel(
            name='GoodsProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('prop_name', models.CharField(verbose_name='商品属性名', max_length=128)),
                ('is_optional', models.BooleanField(verbose_name='是否可选', default=True)),
            ],
            options={
                'verbose_name': '商品属性',
                'verbose_name_plural': '商品属性',
                'db_table': 'fk_goods_property',
            },
        ),
        migrations.CreateModel(
            name='GoodsPropMapp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('prop_value', models.CharField(verbose_name='商品属性值', max_length=256)),
                ('prop', models.ForeignKey(verbose_name='商品属性', to='goods.GoodsProperty')),
            ],
            options={
                'verbose_name': '商品属性映射',
                'verbose_name_plural': '商品属性映射',
                'db_table': 'fk_goods_prop_mapp',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='名称', max_length=128)),
                ('desc', models.CharField(verbose_name='简介', max_length=256)),
                ('image', models.ImageField(verbose_name='图片', upload_to='goods')),
                ('bid_price', models.DecimalField(verbose_name='原价', max_digits=10, decimal_places=2)),
                ('real_price', models.DecimalField(verbose_name='促销价', max_digits=10, decimal_places=2)),
                ('sales', models.IntegerField(verbose_name='销量', default=0)),
                ('comments', models.IntegerField(verbose_name='评价', default=0)),
                ('integral', models.IntegerField(verbose_name='积分', default=1)),
                ('stock', models.IntegerField(verbose_name='库存', default=0)),
                ('status', models.SmallIntegerField(verbose_name='状态', default=1, choices=[(1, '上架'), (0, '下架')])),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情', blank=True)),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'db_table': 'fk_goods_sku',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('type', models.CharField(verbose_name='种类', max_length=64)),
                ('icon', models.CharField(verbose_name='种类图标', max_length=20, null=True)),
            ],
            options={
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
                'db_table': 'fk_goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexSaleActive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='活动名称', max_length=128, null=True)),
                ('image', models.ImageField(verbose_name='图片', null=True, upload_to='index_active')),
                ('url', models.URLField(verbose_name='活动链接')),
                ('display', models.SmallIntegerField(verbose_name='展示区域', choices=[(0, '文字'), (1, '广告位'), (2, 'banner小部分'), (3, '首页大类banner'), (4, 'banner')])),
                ('index', models.SmallIntegerField(verbose_name='展示顺序', default=0)),
            ],
            options={
                'verbose_name': '促销活动',
                'verbose_name_plural': '促销活动',
                'db_table': 'fk_index_active',
            },
        ),
        migrations.CreateModel(
            name='ServerPromise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('promise', models.CharField(verbose_name='承诺', max_length=128)),
                ('mapp', models.ManyToManyField(verbose_name='商品服务承诺映射', to='goods.GoodsSKU', through='goods.GoodsPromiseMapp')),
            ],
            options={
                'verbose_name': '服务承诺',
                'verbose_name_plural': '服务承诺',
                'db_table': 'fk_server_promise',
            },
        ),
        migrations.CreateModel(
            name='IndexBrand',
            fields=[
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('brand', models.OneToOneField(verbose_name='品牌', primary_key=True, serialize=False, to='goods.GoodsBrand')),
                ('url', models.URLField(verbose_name='品牌链接')),
                ('index', models.SmallIntegerField(verbose_name='展示顺序')),
            ],
            options={
                'verbose_name': '首页品牌展示',
                'verbose_name_plural': '首页品牌展示',
                'db_table': 'fk_index_brands',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='brand',
            field=models.ForeignKey(verbose_name='商品品牌', to='goods.GoodsBrand'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods',
            field=models.ForeignKey(verbose_name='商品SPU', to='goods.Goods'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(verbose_name='商品种类', to='goods.GoodsType'),
        ),
        migrations.AddField(
            model_name='goodspropmapp',
            name='sku',
            field=models.ForeignKey(verbose_name='商品SKU', to='goods.GoodsSKU'),
        ),
        migrations.AddField(
            model_name='goodsproperty',
            name='mapp',
            field=models.ManyToManyField(verbose_name='商品属性映射', to='goods.GoodsSKU', through='goods.GoodsPropMapp'),
        ),
        migrations.AddField(
            model_name='goodspromisemapp',
            name='promise',
            field=models.ForeignKey(verbose_name='服务承诺', to='goods.ServerPromise'),
        ),
        migrations.AddField(
            model_name='goodspromisemapp',
            name='sku',
            field=models.ForeignKey(verbose_name='商品SKU', to='goods.GoodsSKU'),
        ),
        migrations.AddField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(verbose_name='商品SKU', to='goods.GoodsSKU'),
        ),
    ]
