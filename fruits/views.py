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
import time
from django.db import transaction

# Create your views here.
def index(request):
    user = User.objects.get(username=request.session.get('login_user'))
    if user:
        total_count=get_car_count(user)
    else:
        total_count=0
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


    content.update(total_count=total_count,user=user)
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
        total_count=get_car_count(user)
    else:
        total_count=0

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
             "user":user,"total_count":total_count,
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

    user = User.objects.get(username=request.session.get('login_user'))
    if user:
        total_count=get_car_count(user)
    else:
        total_count=0
    txt={
        "types":types,"type":type,
        "pages":pages,"my_page":my_page,
        "goodssku_list":goodssku_list,
        "total_count":total_count,
        "sort":sort,"user":user
    }
    return render(request,"fruits/list.html",txt)


@check_user
def add_car(request):
    id = request.GET.get("id")

    num=request.GET.get("num")
    user=User.objects.get(username=request.session.get("login_user"))
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

#查询列表页 获取购物车商品数量
def get_count(request):
    user=request.session.get("login_user")
    if user:
        user=User.objects.get(username=user)
        total_count=get_car_count(user)
    else:
        total_count=0
    return JsonResponse({"total_count": total_count})

@check_user
def check_car(request):
    user=User.objects.get(username=request.session.get("login_user"))

    conn = settings.REDIS_CONN
    car_key = 'car_%d' % user.id
    car_dict = conn.hgetall(car_key)

    skus=[]
    total_count=0
    total_price=0

    for id, num in car_dict.items():
        #根据商品id获取商品信息
        sku = GoodsSKU.objects.get(id=id)
        amount=sku.price * int(num)
        #动态给sku对象增加amount属性,保存商品小计
        sku.amount = amount
        #动态给sku对象增加count属性,保存商品数量
        sku.count=num
        skus.append(sku)

        total_count+=int(num)
        total_price+=amount

    context={
        "total_count":total_count,
        "total_price":total_price,
        "skus":skus,"user":user
    }
    return render(request,"fruits/cart.html",context)

@check_user
def up_car(request):
    user=User.objects.get(username=request.session.get("login_user"))
    id=request.GET.get("sku_id")
    num=int(request.GET.get("count"))
    goodssku=GoodsSKU.objects.get(id=id)

    conn = settings.REDIS_CONN
    car_key = 'car_%d' % user.id

    car_num = conn.hget(car_key, id)
    if car_num:
        num = int(num)
    if num > goodssku.stock:
        return JsonResponse({"res": 4, "errmsg": "商品库存不足"})

    conn.hset(car_key, id, num)
    total_count = get_car_count(user)
    return JsonResponse({"res": 5, "total_count": total_count, "message": "添加成功"})

@check_user
def del_car(request):
    user = User.objects.get(username=request.session.get("login_user"))
    id = request.GET.get("sku_id")

    conn = settings.REDIS_CONN
    car_key = 'car_%d' % user.id

    conn.hdel(car_key, id)

    return JsonResponse({"res": 3,"message": "删除成功"})


@check_user
def place(request):
    user = User.objects.get(username=request.session.get("login_user"))
    total_count = get_car_count(user)

    sku_ids=request.POST.getlist("sku_ids")

    skus=[]
    sku_id=''
    money=0
    num=0

    conn = settings.REDIS_CONN
    car_key = 'car_%d' % user.id
    for i in sku_ids:
        sku=GoodsSKU.objects.get(id=int(i))
        sku.count=conn.hget(car_key, int(i))
        sku.money=int(sku.count) * sku.price

        money+=sku.money
        skus.append(sku)

        i=i+"-"
        sku_id+=i
        num+=1

    sites=Site.objects.filter(u_id=user)

    context={
        "total_count":total_count,"user":user,
        "money":money,"skus":skus,"sku_id":sku_id,
        "sites":sites,"num":num
    }

    return render(request,"fruits/place_order.html",context)


@check_user
@transaction.non_atomic_requests
def add_order(request):
    user = User.objects.get(username=request.session.get("login_user"))
    pay_method=request.GET.get("pay_style")
    site=Site.objects.get(id=request.GET.get("site_id"))

    sku_id=request.GET.get("sku_id")

    sku_id=sku_id.split("-")

    conn = settings.REDIS_CONN
    car_key = 'car_%d' % user.id
    skus=[]
    moneys=0
    tim=int(time.time())
    order_id='%s_%s'%(tim,user.id)
    ordergoods_list=[]

    # 创建保存点
    sid = transaction.savepoint()
    try:
        order = Order.objects.create(order_id=order_id,user=user,pay_method=pay_method,
                                     count=0,order_money=0,status=1)
        ordersite=OrderSite.objects.create(order=order,name=site.sitename,address=site.address,phone=site.sitephone)

        for i in sku_id:
            if i:
                print(i)
                sku=GoodsSKU.objects.get(id=i)
                count = int(conn.hget(car_key,int(i)))
                if count>sku.stock:
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({"res": 1,"message": "库存不足"})
                money=count * sku.price
                print(money)
                moneys+=money
                #删除购物车中商品
                conn.hdel(car_key,i)
                #修改商品库存
                GoodsSKU.objects.filter(id=i).update(stock=sku.stock-count)
                #添加订单详情
                ordergoods=OrderGoods.objects.create(order=order,name=sku.name,price=sku.price,
                                                     count=count,money=money,goods=sku)
                ordergoods_list.append(ordergoods)

        order.count=len(sku_id) -1
        order.order_money=moneys
        order.save()
        transaction.savepoint_commit(sid)
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(sid)
        return JsonResponse({"res": 2, "message": "%s"%e})
    context={
        "user":user,"ordersite":ordersite,"order":order,
        'ordergoods_list':ordergoods_list,
    }
    return redirect(reverse("fruits:check_order"))


@check_user
def check_order(request):
    user = User.objects.get(username=request.session.get("login_user"))

    order1_l=[]
    order2_l=[]
    order_1=Order.objects.filter(user=user,status=1)
    print(len(order_1))
    for order in order_1:
        ordergoods=OrderGoods.objects.filter(order=order)
        for i in ordergoods:
            order1_l.append(i)
    print(len(order1_l))
    order_2=Order.objects.filter(user=user,status__gt=1)
    for order in order_2:
        ordergoods = OrderGoods.objects.filter(order=order)
        for i in ordergoods:
            order2_l.append(i)

    context={
        "user":user,"order1_l":order1_l,"order2_l":order2_l,
        "order_1":order_1,"order_2":order_2
    }
    return render(request,"user/user_center_order.html",context)
