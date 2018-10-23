from django.shortcuts import render
from fruits.models import *
from django.core.cache import cache

# Create your views here.
def index(request):
    content = cache.get('cache_index')
    if content==None:
        print("设置缓存")
        types = GoodsType.objects.all()

        goods_banners=IndexGoodsBanner.objects.all()

        promotion_banners=IndexPromotionBanner.objects.all()

        for type in types:
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type,display_type=1).order_by("index")
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type,display_type=0).order_by("index")

            type.image_banners = image_banners
            type.title_banners = title_banners

        content = {
            'types':types,
            'goods_banners':goods_banners,
            'promotion_banners':promotion_banners,
        }

        cache.set('cache_index',content,3600)

    car_count=0
    content.update(car_count=car_count)
    return render(request,"fruits/index.html",content)


def detail(request,id):
    types=GoodsType.objects.all()
    goodssku=GoodsSKU.objects.get(id=id)
    goodsspu=Goods.objects.get(id=goodssku.goods_id)
    goodssku_list=GoodsSKU.objects.filter(type=goodssku.type)

    return render(request,"fruits/detail.html",{"goodssku":goodssku,"types":types,"goodsspu":goodsspu,"goodssku_list":goodssku_list})

