from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=36,null=False)
    phone = models.CharField(max_length=11)
    email = models.EmailField(null=False)
    is_activate = models.BooleanField(default=False)
    # address = models.CharField(max_length=50, blank=True, null=True)

    isDelete = models.BooleanField(default=False)

class Site(models.Model):
    sitename = models.CharField(max_length=20)
    sitephone = models.CharField(max_length=11)
    address = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)
    u_id = models.ForeignKey(User)