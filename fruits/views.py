from django.shortcuts import render
from fruits.models import *

# Create your views here.
def index(request):
    types = GoodsType.objects.all()

    goods_banners=IndexGoodsBanner.objects.all()

    promotion_banners=IndexPromotionBanner.objects.all()

    for type in types:
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type,display_type=1).order_by("index")
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type,display_type=0).order_by("index")

        type.image_banners = image_banners
        type.title_banners = title_banners

    # goodssku_list=GoodsSKU.objects.all()
    return render(request,"fruits/index.html",{"types":types,"goods_banners":goods_banners,
                                               "promotion_banners":promotion_banners,})