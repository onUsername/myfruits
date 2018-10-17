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
                ('areaid', models.AutoField(primary_key=True, db_column='areaId', serialize=False)),
                ('areacode', models.CharField(max_length=50, db_column='areaCode')),
                ('areaname', models.CharField(max_length=20, db_column='areaName')),
                ('level', models.IntegerField(blank=True, null=True)),
                ('citycode', models.CharField(blank=True, max_length=50, db_column='cityCode', null=True)),
                ('center', models.CharField(blank=True, max_length=50, null=True)),
                ('parentid', models.IntegerField(blank=True, db_column='parentId', null=True)),
            ],
            options={
                'db_table': 'T_Area',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=36)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.CharField(max_length=254)),
                ('is_activate', models.BooleanField(default=False)),
                ('isdelete', models.IntegerField(db_column='isDelete')),
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
