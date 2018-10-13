import hashlib
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import uuid,os

def my_md5(value):
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    return m.hexdigest()


def check_user(func):
    def inner(*args, **kwargs):
        username = args[0].session.get("login_user", "")
        if username == "":
            args[0].session["path"] = args[0].path
            args[0].session["error_link"] = "请先进行登录"
            return redirect(reverse("user:login"))
        return func(*args, **kwargs)

    return inner


def do_file_name(file_name):
    return str(uuid.uuid1())+os.path.splitext(file_name)[1]