from celery import Celery
from django.core.mail import send_mail
from django.template import RequestContext,loader
from django.conf import settings


# celery -A utils.tesk worker -l info

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myfruits.settings")
django.setup()

from fruits.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner

app =Celery("utils.tesk",broker="redis://192.168.12.216:6379/3")

@app.task
def task_send_mail(subject,message,sender,receiver,html_message):
    import time
    print("发送邮件begin..")
    send_mail(subject,message,sender,receiver,html_message=html_message)
    print("发邮件end...")


@app.task
def task_generate_static_index():
    """产生静态首页"""
    print("生成静态首页begin..")
    types = GoodsType.objects.all()

    goods_banners = IndexGoodsBanner.objects.all()

    promotion_banners = IndexPromotionBanner.objects.all()

    for type in types:
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by("index")
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by("index")

        type.image_banners = image_banners
        type.title_banners = title_banners

    cart_count = 0
    context={
        'types':types,
        'goods_banners':goods_banners,
        'promotion_banners':promotion_banners,
        'car_count':cart_count
    }

    temp = loader.get_template('fruits/index.html')
    static_index_html = temp.render(context)
    save_path=os.path.join(settings.BASE_DIR,'static/html/index.html')
    with open(save_path,'w')as f:
        f.write(static_index_html)
    print("生成静态首页end...")
