from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from django.core.mail import send_mail
from user.models import *

from utils.views_util import *
from utils.user_util import *
from utils.tesk import task_send_mail

from django.http import HttpResponse
from io import BytesIO

import urllib,json
from myfruits import settings


from django.http import *

from django.core import serializers
# Create your views here.

def check_username(request):
    username = request.GET.get("username")
    print(username)
    for i in User.objects.all():
        if i.username == username:
            r={"r_link":"该用户名已被使用"}
            return HttpResponse(json.dumps(r, ensure_ascii=False),
                                content_type="application/json;charset=utf-8")
    else:
        if len(username)>=6 and len(username)<=10:
            r = {"r_link": ""}

            return HttpResponse(json.dumps(r, ensure_ascii=False),
                            content_type="application/json;charset=utf-8")
        else:
            r = {"r_link": "用户名为6-10位"}

            return HttpResponse(json.dumps(r, ensure_ascii=False),
                                content_type="application/json;charset=utf-8")


def check_password(request):
    password = request.POST.get("password")
    print(password)

    if len(password)>=6 and len(password)<=10:
        r = {"r_link": ""}
        # return HttpResponse(json.dumps(r, ensure_ascii=False),
        #                 content_type="application/json;charset=utf-8")
    else:
        r = {"r_link": "密码为6-10位"}
    return HttpResponse(json.dumps(r, ensure_ascii=False),
                        content_type="application/json;charset=utf-8")

def check_password2(request):
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    print(password,password2)
    if password==password2:
        r = {"r_link": ""}
        # return HttpResponse(json.dumps(r, ensure_ascii=False),
        #                     content_type="application/json;charset=utf-8")
    else:
        r = {"r_link": "两次密码不一致"}

    return HttpResponse(json.dumps(r, ensure_ascii=False),
                            content_type="application/json;charset=utf-8")

def check_img_code(request):
    img_code1 = request.GET.get("img_code").lower()
    img_code2= request.session.get("img_code").lower()
    print(img_code1,img_code2)
    if img_code1==img_code2:
        r = {"r_link": ""}
    else:
        r = {"r_link": "验证码错误"}
    return HttpResponse(json.dumps(r, ensure_ascii=False),
                            content_type="application/json;charset=utf-8")

def create_img_code(request):
    # 在内存中开辟空间生成临时的图片
    f = BytesIO()
    # 生成图片和验证码
    img, code =create_code()
    #将验证码保存到session中
    print(code)
    print(1)
    request.session["img_code"]=code
    #将图片储存在IO
    img.save(f,"PNG")
    return HttpResponse(f.getvalue())

def register(request):
    if request.method == "GET":
        return render(request, "user/register.html")
    else:
        img_code = request.POST.get("img_code","").strip().lower()
        if img_code != request.session.get("img_code").lower():
            return render(request,"user/register.html",{"error_link":"验证码错误"})
        username = request.POST.get("user_name", "").strip()
        password = request.POST.get("pwd", "").strip()
        email = request.POST.get("email", "").strip()
        if User.objects.all:
            for i in User.objects.all():
                if i.username == username:
                    return render(request, "user/register.html", {"error_link": "该用户名已存在"})
        #     else:
        #         pass
        # else:
        #     pass

        if len(username) >= 6 and len(username) <= 10:
            if len(password) >= 6 and len(password) <= 10:
                user = User.objects.create(username=username, password=my_md5(password),email=email)

                serializer = Serializer(settings.SECRET_KEY, 3600)
                info = {"confirm": user.id}
                token = serializer.dumps(info).decode()
                encrytion_url = "http://192.168.12.216:8888/user/active/%s"%token

                subject = "天天生鲜欢迎信息"
                message = ""
                sender = settings.EMAIL_FROM
                receiver = [email]
                html_message = "<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面的链接激活你的账户<br/><a href='%s'>%s</a>"%(username,encrytion_url,encrytion_url)
                print(subject)
                task_send_mail.delay(subject,message,sender,receiver,html_message)

                return redirect(reverse("user:login"))
            else:
                return render(request, "user/register.html", {"error_link": "密码为6-10位"})
        else:
            return render(request, "user/register.html", {"error_link": "用户名为6-10位"})


def active(request,token):
    # token = request.GET.get("token")
    serializer = Serializer(settings.SECRET_KEY,3600)
    try:
        info =serializer.loads(token)
        user_id =info['confirm']

        user = User.objects.get(id=user_id)
        user.is_activate =1
        user.save()
        return redirect(reverse("user:login"))
    except SignatureExpired as e:
        return HttpResponse("激活链接已过期")
    except BadSignature as e:
        return HttpResponse("激活链接非法")

def forget_password(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = User.objects.get(username=username)

    serializer = Serializer(settings.SECRET_KEY, 3600)
    info = {"confirm": user.id,"pass":password}
    token = serializer.dumps(info).decode()
    encrytion_url = "http://192.168.12.216:8888/user/reset_password/%s" % token

    subject = "天天生鲜密码重置"
    message = ""
    sender = settings.EMAIL_FROM
    receiver = [user.email]
    html_message = "<h1>%s,你正在重置密码</h1>请点击下面的链接重置你的密码<br/><a href='%s'>%s</a>" % (
    username, encrytion_url, encrytion_url)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    r = {"r_link": "请前往注册邮箱进行密码重置"}

    return HttpResponse(json.dumps(r, ensure_ascii=False),
                        content_type="application/json;charset=utf-8")


def reset_password(request,token):
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        user_id = info['confirm']
        password = info["pass"]
        user = User.objects.get(id=user_id)
        user.password = my_md5(password)
        user.save()
        return redirect(reverse("user:login"))
    except SignatureExpired as e:
        return HttpResponse("激活链接已过期")
    except BadSignature as e:
        return HttpResponse("激活链接非法")


def login(request):
    if request.method == "GET":
        remember_user_name = request.COOKIES.get("remember_user_name", "")
        error_link = request.session.get("error_link","")
        if request.session.get("error_link"):
            del request.session["error_link"]
        return render(request, "user/login.html", {"remember_user_name": remember_user_name,
                                                   "error_link":error_link})
    else:
        # img_code = request.POST.get("img_code", "").strip().lower()
        # if img_code != request.session.get("img_code").lower():
        #     return render(request, "user/login.html", {"error_link": "验证码错误"})
        username = request.POST.get("username", "").strip()
        password = request.POST.get("pwd", "").strip()
        remember = request.POST.get("remember")
        # print(remember)
        user = User.objects.filter(username=username, password=my_md5(password))
        if user:
            if user[0].is_activate:
                request.session["login_user"] = username
                # request.session["login_user_id"] = user[0].id
                # 得到session中保存的路径
                # print(request.session.get("path"))

                if request.session.get("path"):
                    resp = redirect(request.session.get("path"))
                    del request.session["path"]
                else:
                    resp = redirect(reverse("user:user_center_info"))
                if remember == "1":
                    resp.set_cookie("remember_user_name", username, 3600 * 24 * 7)
                else:
                    resp.set_cookie("remrmber_user_name", username, 0)
                return resp
            else:
                return render(request, "user/login.html", {"error_link": "此帐号尚未激活，请前往注册邮箱激活"})
        else:
            return render(request, "user/login.html", {"error_link": "账号或密码错误"})



def logout(request):
    request.session.flush()
    return redirect(reverse("user:login"))

@check_user
def user_center_info(request):
    login_user = request.session.get("login_user")
    user = User.objects.get(username=login_user)
    return render(request,"user/user_center_info.html",{"login_user":login_user,"user":user})

@check_user
def user_update(request):
    if request.method == "GET":
        login_user = request.session.get("login_user")
        user = User.objects.get(username=login_user)
        return render(request, "user/user_update.html", {"login_user": login_user, "user": user})
    else:
        login_user=request.session.get("login_user")
        user = User.objects.get(username=login_user)
        # password1 =request.POST.get("password1")
        # if user.password!=my_md5(password1):
        #     return render(request, "user/user_update.html", {"login_user": login_user, "error_link": "密码不正确"})
        # username = request.POST.get("username","").strip()
        # password2 = request.POST.get("password2", "").strip()
        phone = request.POST.get("phone").strip()
        email = request.POST.get("email").strip()
        # adddress = request.POST.get("address", "").strip()
        # if len(password2)>=6 and len(password2)<=10:
        #     user.password = my_md5(password2)
        user.phone = phone
        user.email=email
        user.save()
        return redirect(reverse("user:user_center_site"))
        # return render(request,"user/user_update.html",{"login_user":login_user,"user":user,
        #                                                "error_link":"密码必须为6-10位"})


@check_user
def user_center_site(request):
    user = User.objects.get(username=request.session.get("login_user"))
    default_site_list = Site.objects.filter(u_id=user,is_default=True)
    site_list = Site.objects.filter(u_id=user,is_default=False)

    return render(request,"user/user_center_site.html",{"site_list":site_list,"user":user,"default_site_list":default_site_list})


@check_user
def add_site(request):
    if request.method=="GET":
        return render(request,"user/add_site.html")
    else:
        user = User.objects.get(username=request.session.get("login_user"))
        sitename= request.POST.get("sitename")
        sitephone = request.POST.get("sitephone")

        sheng =  TArea.objects.get(areaid=request.POST.get("sheng_id")).areaname
        shi =  TArea.objects.get(areaid=request.POST.get("shi_id")).areaname
        xian = TArea.objects.get(areaid=request.POST.get("xian_id")).areaname
        detail_address = request.POST.get("detail_address")

        address = "%s-%s-%s-%s"%(sheng,shi,xian,detail_address)
        print(address)
        is_default = request.POST.get("is_default")

        site= Site.objects.create(sitename=sitename,sitephone=sitephone,address=address,u_id=user)

        if is_default:
            try:
                site_li = Site.objects.get(u_id=user,is_default=True)
                site_li.is_default =False
                site_li.save()
                site.is_default = True
            except:
                site.is_default=True
        else:
            site.is_default = False
        site.save()
        return redirect(reverse("user:user_center_site"))


@check_user
def update_site(request,id):
    if request.method=="GET":

        site = Site.objects.get(id=id)
        address=site.address
        address_list = address.split("-")



        TArea_sheng = TArea.objects.filter(parentid=-1)

        sheng_id = TArea.objects.get(areaname=address_list[0]).areaid

        TArea_shi = TArea.objects.filter(parentid=sheng_id)

        shi_id = TArea.objects.get(areaname=address_list[1],parentid=sheng_id).areaid
        TArea_xian = TArea.objects.filter(parentid=shi_id)

        xian_id = TArea.objects.get(areaname=address_list[2],parentid=shi_id).areaid

        detail_address = address_list[3]

        return render(request,"user/update_site.html",{"site":site,"id":id,"TArea_sheng":TArea_sheng,"TArea_shi":TArea_shi,"TArea_xian":TArea_xian,
                                                       "sheng_id":sheng_id,"shi_id":shi_id,"xian_id":xian_id,"detail_address":detail_address})
    else:
        user = User.objects.get(username=request.session.get("login_user"))
        site = Site.objects.get(id=id)
        site.sitename = request.POST.get("sitename")

        sheng = TArea.objects.get(areaid=request.POST.get("sheng_id")).areaname
        shi = TArea.objects.get(areaid=request.POST.get("shi_id")).areaname
        xian = TArea.objects.get(areaid=request.POST.get("xian_id")).areaname
        detail_address = request.POST.get("detail_address")

        address = "%s-%s-%s-%s" % (sheng, shi, xian, detail_address)

        site.address = address
        site.sitephone = request.POST.get("sitephone")
        site.u_id = user
        is_default = request.POST.get("is_default")

        if is_default:
            try:
                site_li = Site.objects.get(u_id=user,is_default=True)
                site_li.is_default =False
                site_li.save()
                site.is_default = True
            except:
                site.is_default=True
        else:
            site.is_default = False
        site.save()
        return redirect(reverse("user:user_center_site"))


@check_user
def del_site(request,id):
    Site.objects.get(id=id).delete()
    return redirect(reverse("user:user_center_site"))



def seach_sheng(request):
    sheng_list = TArea.objects.filter(parentid=-1)
    print(sheng_list)
    content = {
        "sheng_list":serializers.serialize("json",sheng_list)
    }
    return JsonResponse(content)

def seach_shi(request):
    sheng_id = request.GET.get("sheng_id")
    shi_list = TArea.objects.filter(parentid=sheng_id)
    content = {
        "shi_list":serializers.serialize("json",shi_list)
    }
    return JsonResponse(content)

def seach_xian(request):
    shi_id = request.GET.get("shi_id")
    print(shi_id)
    xian_list = TArea.objects.filter(parentid=shi_id)
    print(xian_list)
    content = {
        "xian_list":serializers.serialize("json",xian_list)
    }
    return JsonResponse(content)

def index(requests):
    return render(requests, "user/index.html")
