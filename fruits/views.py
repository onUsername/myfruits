from django.shortcuts import render
from fruits.models import *
from django.core.cache import cache
from user.models import *
from redis import StrictRedis

# Create your views here.
def index(request):
    user=User.objects.get(username=request.session.get('login_user'))
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
    content.update(car_count=car_count,user=user)
    return render(request,"fruits/index.html",content)


def detail(request,id):
    user = User.objects.get(username=request.session.get('login_user'))
    if user:
        #添加用户的历史记录
        conn = StrictRedis('192.168.12.216')
        history_key='history_%d'% user.id
        #移除列表中的id
        conn.lrem(history_key,0,id)
        #把商品id插入列表左侧
        conn.lpush(history_key,id)
        #只保存用户最新浏览的5条信息
        conn.ltrim(history_key,0,4)

    types=GoodsType.objects.all()
    goodssku=GoodsSKU.objects.get(id=id)
    goodsspu=Goods.objects.get(id=goodssku.goods_id)
    #相同type下的其他sku两个
    goodssku_list=GoodsSKU.objects.filter(type=goodssku.type).order_by("-id")[:2]
    #相同spu下的其他sku，除了自身
    same_spu_sku=GoodsSKU.objects.filter(goods=goodssku.goods).exclude(id=goodssku.id)

    content={"goodssku":goodssku,
             "types":types,
             "goodsspu":goodsspu,
             "goodssku_list":goodssku_list,
             "user":user,
             "same_spu_sku":same_spu_sku}
    return render(request,"fruits/detail.html",content)

