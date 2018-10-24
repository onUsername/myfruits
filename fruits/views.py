from django.shortcuts import render,redirect
from fruits.models import *
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from user.models import *
from redis import StrictRedis
from utils.user_util import *
from django.http import *
from myfruits import settings


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


def list(request,type_id,pn):
    sort=request.GET.get('sort')
    try:
        type=GoodsType.objects.get(id=type_id)
    except:
        return redirect(reverse("fruits:index"))
    types=GoodsType.objects.all()
    #新品推荐
    goodssku_list = GoodsSKU.objects.filter(type=type_id).order_by("-id")[:2]
    #按类行排序
    if sort=='1':
        sku_list=GoodsSKU.objects.filter(type=type_id).order_by('-id')
    elif sort=='2':
        sku_list = GoodsSKU.objects.filter(type=type_id).order_by('price')
    else:
        sku_list = GoodsSKU.objects.filter(type=type_id).order_by('sales')
    my_paginator=Paginator(sku_list,1)

    try:
        pn=int(pn)
    except:
        pn=1
    if pn>my_paginator.num_pages:
        pn=my_paginator.num_pages
    elif pn<1:
        pn=1

    my_page=my_paginator.page(pn)

    """
    总页面小于5页，显示所有页码
    当前页面前3页,显示1-5页
    当前页面后3页，显示后5页
    
    """
    num_page = my_paginator.num_pages
    if num_page<5:
        pages = range(1,num_page+1)
    elif pn<=3:
        pages = range(1,6)
    elif num_page-pn <= 2:
        pages = range(num_page-4,num_page+1)
    else:
        pages = range(pn-2,pn+3)

    car_count=0
    txt={
        "types":types,"type":type,
        "pages":pages,"my_page":my_page,
        "goodssku_list":goodssku_list,
        "car_count":car_count,
        "sort":sort
    }
    return render(request,"fruits/list.html",txt)


@check_user
def add_car(request):
    id = request.GET.get("id")

    num=request.GET.get("num")
    user=User.objects.get(username=request.session.get("login_user"))
    print(user)
    if not all([id,num]):
        return JsonResponse({'res':1})
    #检测商品数量
    try:
        num=int(num)
    except:
        return JsonResponse({'res':2,"errmsg":"商品数目出错"})
    #检测商品是否存在
    try:
        goodssku = GoodsSKU.objects.get(id=id)
    except:
        return JsonResponse({'res': 3, "errmsg": "商品不存在"})

    conn=settings.REDIS_CONN
    car_key='car_%d' % user.id

    car_num=conn.hget(car_key,id)
    if car_num:
        num+=int(car_num)
    if num>goodssku.stock:
        return JsonResponse({"res":4,"errmsg":"商品库存不足"})

    conn.hset(car_key,id,num)

    #计算用户购物车商品条数
    total_count=get_car_count(user)
    return JsonResponse({"res":5,"total_count":total_count,"message":"添加成功"})


def get_car_count(user):

    total_count=0

    conn=settings.REDIS_CONN
    car_key='car_%d' % user.id
    car_dict=conn.hgetall(car_key)

    for id,num in car_dict.items():
        total_count+=int(num)
    return total_count