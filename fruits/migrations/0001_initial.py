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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='商品SPU名称', max_length=100)),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情', blank=True)),
            ],
            options={
                'verbose_name_plural': '商品SPU',
                'verbose_name': '商品SPU',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(verbose_name='图片路径', upload_to='')),
            ],
            options={
                'verbose_name_plural': '商品图片',
                'verbose_name': '商品图片',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='商品名称', max_length=100)),
                ('desc', models.CharField(verbose_name='商品简介', max_length=256)),
                ('price', models.DecimalField(decimal_places=2, verbose_name='商品价格', max_digits=10)),
                ('unite', models.CharField(verbose_name='商品单位', max_length=20)),
                ('image', models.ImageField(verbose_name='商品图片', upload_to='')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('status', models.SmallIntegerField(default=1, verbose_name='商品状态', choices=[(0, '下线'), (1, '上线')])),
                ('goods', models.ForeignKey(to='fruits.Goods', verbose_name='商品SPU ')),
            ],
            options={
                'verbose_name_plural': '商品',
                'verbose_name': '商品',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='种类名称', max_length=100)),
                ('image', models.ImageField(verbose_name='商品类型图片', upload_to='')),
            ],
            options={
                'verbose_name_plural': '商品种类',
                'verbose_name': '商品种类',
            },
        ),
        migrations.CreateModel(
            name='IndexGoodsBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(verbose_name='图片', upload_to='')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('sku', models.ForeignKey(to='fruits.GoodsSKU', verbose_name='商品')),
            ],
            options={
                'db_table': 'df_index_banner',
                'verbose_name_plural': '首页轮播商品',
                'verbose_name': '首页轮播商品',
            },
        ),
        migrations.CreateModel(
            name='IndexPromotionBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='活动名称', max_length=20)),
                ('url', models.CharField(verbose_name='活动链接', max_length=256)),
                ('image', models.ImageField(verbose_name='活动图片', upload_to='')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
            ],
            options={
                'db_table': 'df_index_promotion',
                'verbose_name_plural': '主页活动促销',
                'verbose_name': '主页活动促销',
            },
        ),
        migrations.CreateModel(
            name='IndexTypeGoodsBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('display_type', models.SmallIntegerField(default=1, verbose_name='展示类型', choices=[(0, '标题'), (1, '图片')])),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('sku', models.ForeignKey(to='fruits.GoodsSKU', verbose_name='商品SKU')),
                ('type', models.ForeignKey(to='fruits.GoodsType', verbose_name='商品类型')),
            ],
            options={
                'db_table': 'df_index_type_goods',
                'verbose_name_plural': '主页分类展示商品',
                'verbose_name': '主页分类展示商品',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(to='fruits.GoodsType', verbose_name='商品种类'),
        ),
        migrations.AddField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(to='fruits.GoodsSKU', verbose_name='商品'),
        ),
    ]
