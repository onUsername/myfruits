# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodstype',
            name='logo',
            field=models.CharField(max_length=10, default='fruits', verbose_name='标签'),
        ),
    ]
