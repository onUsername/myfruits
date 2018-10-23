from django.contrib import admin

# Register your models here.
from fruits.models import *
from django.core.cache import cache

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表中数据时调用"""
        from utils.tesk import task_generate_static_index
        super().save_model(request,obj,form,change)
        task_generate_static_index.delay()
        cache.delete("cache_index")

    def delete_model(self, request, obj):
        from utils.tesk import task_generate_static_index
        super().delete_model(request,obj)
        task_generate_static_index.delay()
        cache.delete("cache_index")


admin.site.register(GoodsType)
admin.site.register(Goods)
admin.site.register(GoodsSKU,BaseAdmin)
admin.site.register(GoodsImage)

admin.site.register(IndexGoodsBanner,BaseAdmin)
admin.site.register(IndexTypeGoodsBanner,BaseAdmin)
admin.site.register(IndexPromotionBanner,BaseAdmin)
