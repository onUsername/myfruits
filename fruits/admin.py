from django.contrib import admin

# Register your models here.
from fruits.models import *
admin.site.register(GoodsType)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)

admin.site.register(IndexGoodsBanner)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexPromotionBanner)
