# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockGoodsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='首页区域分类名', max_length=50)),
                ('en_name', models.CharField(verbose_name='首页区域分类名英文', max_length=128)),
                ('image', models.ImageField(verbose_name='分类图片', upload_to='block_goods_type')),
                ('style', models.CharField(verbose_name='样式名', max_length=50, blank=True, null=True)),
                ('url', models.CharField(verbose_name='区域banner链接', max_length=256, blank=True, null=True)),
                ('index', models.SmallIntegerField(verbose_name='展示顺序')),
                ('father_type', models.ForeignKey(verbose_name='所属分类', blank=True, null=True, to='goods.BlockGoodsType')),
            ],
            options={
                'verbose_name': '首页商品区块',
                'verbose_name_plural': '首页商品区块',
                'db_table': 'fk_block_goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('index', models.SmallIntegerField(verbose_name='展示顺序')),
                ('block_type', models.ForeignKey(verbose_name='所属分类', to='goods.BlockGoodsType')),
                ('sku', models.ForeignKey(verbose_name='商品sku', to='goods.GoodsSKU')),
            ],
            options={
                'verbose_name': '首页商品',
                'verbose_name_plural': '首页商品',
                'db_table': 'fk_index_goods',
            },
        ),
        migrations.AlterField(
            model_name='goodsbrand',
            name='logo',
            field=models.ImageField(verbose_name='品牌logo', blank=True, null=True, upload_to='goods_brand'),
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='icon',
            field=models.CharField(verbose_name='种类图标', max_length=20, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indexsaleactive',
            name='name',
            field=models.CharField(verbose_name='活动名称', max_length=128, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indexsaleactive',
            name='url',
            field=models.CharField(verbose_name='活动链接', max_length=256, blank=True),
        ),
    ]
