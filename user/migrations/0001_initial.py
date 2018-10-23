# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sitename', models.CharField(max_length=20)),
                ('sitephone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=120)),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user_site',
            },
        ),
        migrations.CreateModel(
            name='TArea',
            fields=[
                ('areaid', models.AutoField(db_column='areaId', primary_key=True, serialize=False)),
                ('areacode', models.CharField(db_column='areaCode', max_length=50)),
                ('areaname', models.CharField(db_column='areaName', max_length=20)),
                ('level', models.IntegerField(null=True, blank=True)),
                ('citycode', models.CharField(db_column='cityCode', null=True, blank=True, max_length=50)),
                ('center', models.CharField(null=True, blank=True, max_length=50)),
                ('parentid', models.IntegerField(db_column='parentId', null=True, blank=True)),
            ],
            options={
                'db_table': 'T_Area',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('username', models.CharField(unique=True, max_length=20)),
                ('password', models.CharField(max_length=36)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=254)),
                ('is_activate', models.BooleanField(default=False)),
                ('isdelete', models.IntegerField(db_column='isDelete', default=False)),
            ],
            options={
                'db_table': 'user_user',
            },
        ),
        migrations.AddField(
            model_name='site',
            name='u_id',
            field=models.ForeignKey(to='user.User'),
        ),
    ]
