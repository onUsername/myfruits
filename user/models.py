# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class TArea(models.Model):
    areaid = models.AutoField(db_column='areaId', primary_key=True)  # Field name made lowercase.
    areacode = models.CharField(db_column='areaCode', max_length=50)  # Field name made lowercase.
    areaname = models.CharField(db_column='areaName', max_length=20)  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)
    citycode = models.CharField(db_column='cityCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    center = models.CharField(max_length=50, blank=True, null=True)
    parentid = models.IntegerField(db_column='parentId', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return ("name=%s"%self.areaname)

    class Meta:
        managed = False
        db_table = 'T_Area'




class Site(models.Model):
    sitename = models.CharField(max_length=20)
    sitephone = models.CharField(max_length=11)
    address = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)
    u_id = models.ForeignKey('User')

    class Meta:
        managed = False
        db_table = 'user_site'


class User(models.Model):
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=36)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=254)
    is_activate = models.BooleanField(default=False)
    isdelete = models.IntegerField(db_column='isDelete')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_user'
