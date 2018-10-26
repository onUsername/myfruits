from django.db import models
from tinymce.models import HTMLField
# from user.models import *

# Create your models here.

class GoodsType(models.Model):
    name = models.CharField(max_length=100,verbose_name="种类名称")
    # image = models.ImageField(upload_to="type",verbose_name="商品类型图片")
    image = models.ImageField(verbose_name="商品类型图片")
    logo = models.CharField(max_length=10,verbose_name='标签',default='fruits')
    class Meta:
        verbose_name = "商品种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(models.Model):
    status_choices = (
        (0,"下线"),
        (1,"上线")
    )
    type = models.ForeignKey("GoodsType",verbose_name="商品种类")
    goods=models.ForeignKey("Goods",verbose_name="商品SPU ")
    name = models.CharField(max_length=100,verbose_name="商品名称")
    desc = models.CharField(max_length=256,verbose_name="商品简介")
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品价格")
    unite = models.CharField(max_length=20,verbose_name="商品单位")
    # image = models.ImageField(upload_to="goods",verbose_name="商品图片")
    image = models.ImageField(verbose_name="商品图片")
    stock = models.IntegerField(default=1,verbose_name="商品库存")
    sales = models.IntegerField(default=0,verbose_name="商品销量")
    status = models.SmallIntegerField(default=1,choices=status_choices,verbose_name="商品状态")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=100,verbose_name="商品SPU名称")
    detail = HTMLField(blank=True,verbose_name="商品详情")

    class Meta:
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    sku = models.ForeignKey("GoodsSKU",verbose_name="商品")
    image = models.ImageField(verbose_name="图片路径")
    # image = models.ImageField(upload_to="goods", verbose_name="图片路径")
    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name


class IndexGoodsBanner(models.Model):
    """首页轮播商品展示模型类"""
    sku = models.ForeignKey('GoodsSKU',verbose_name='商品')
    image = models.ImageField(verbose_name='图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name='首页轮播商品'
        verbose_name_plural=verbose_name


class IndexTypeGoodsBanner(models.Model):
    """首页分类商品展示模型类"""
    DISPLAY_TYPE_CHOICES=(
        (0,"标题"),
        (1,"图片")
    )
    type = models.ForeignKey('GoodsType',verbose_name="商品类型")
    sku = models.ForeignKey("GoodsSKU",verbose_name="商品SKU")
    display_type = models.SmallIntegerField(default=1,choices=DISPLAY_TYPE_CHOICES,verbose_name="展示类型")
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')
    class Meta:
        db_table='df_index_type_goods'
        verbose_name = '主页分类展示商品'
        verbose_name_plural=verbose_name



class IndexPromotionBanner(models.Model):
    name = models.CharField(max_length=20,verbose_name='活动名称')
    # url = models.URLField(verbose_name='活动链接')
    url = models.CharField(max_length=256,verbose_name='活动链接')
    image = models.ImageField(verbose_name='活动图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table='df_index_promotion'
        verbose_name='主页活动促销'
        verbose_name_plural=verbose_name


class GoodsComment(models.Model):
    user=models.ForeignKey('user.User')
    goods=models.ForeignKey('GoodsSKU')
    com=models.CharField(max_length=256,verbose_name='评论')
    com_time=models.TimeField()
    pid=models.ForeignKey('GoodsComment',default=-1)




class Order(models.Model):
    PAY_METHOD=(
        (1,"货到付款"),
        (2,"微信支付"),
        (3,"支付宝"),
        (4,"银联支付")
    )
    ORDER_STATUS=(
        (1,"待支付"),
        (2,"代发货"),
        (3,"代收货"),
        (4,"待评价"),
        (5,"已完成")
    )
    order_id=models.CharField(max_length=128,primary_key=True,verbose_name="订单id")
    user=models.ForeignKey("user.User",verbose_name="用户")
    status=models.SmallIntegerField(choices=ORDER_STATUS,default=1,verbose_name="订单状态")
    pay_method=models.SmallIntegerField(choices=ORDER_STATUS,default=3,verbose_name="付款方式")
    count = models.IntegerField(default=1, verbose_name="商品数量")
    order_money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")



class OrderGoods(models.Model):
    """订单详情"""
    order=models.ForeignKey("Order",verbose_name="订单")
    name=models.CharField(max_length=50,verbose_name="商品名称")
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品单价")
    count=models.IntegerField(default=1,verbose_name="商品数量")
    money=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品价格")
    goods=models.ForeignKey("GoodsSKU",verbose_name="商品",default=1)


class OrderSite(models.Model):
    """订单地址"""
    order=models.ForeignKey("Order",verbose_name="订单")
    name=models.CharField(max_length=50,verbose_name="收货人")
    address=models.CharField(max_length=100,verbose_name="具体收货地址")
    phone=models.CharField(max_length=15,verbose_name="收货人电话")

