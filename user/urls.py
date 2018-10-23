from django.conf.urls import include,url
from user import views

urlpatterns = [
    url(r"^check_username/$",views.check_username,name="check_username"),
    url(r"^check_password/$",views.check_password,name="check_password"),
    url(r"^check_password2/$",views.check_password2,name="check_password2"),
    url(r"^check_img_code$",views.check_img_code,name="check_img_code"),



    url(r"^register/$",views.register,name="register"),
    url(r"^active/(?P<token>.*)$",views.active,name="active"),
    url(r"^login/$",views.login,name="login"),
    url(r"^logout/$",views.logout,name="logout"),
    url(r"^create_img_code$",views.create_img_code,name="create_img_code"),

    url(r"^user_center_info/$",views.user_center_info,name="user_center_info"),
    url(r"^forget_password/$", views.forget_password, name="forget_password"),
    url(r"^reset_password/(?P<token>.*)$", views.reset_password, name="reset_password"),
    url(r"^user_update/$",views.user_update,name="user_update"),

    url(r"user_center_site/$",views.user_center_site,name="user_center_site"),
    url(r"add_site/$",views.add_site,name="add_site"),
    url(r"update_site/(\d+)$",views.update_site,name="update_site"),
    url(r"del_site/(\d+)$",views.del_site,name="del_site"),

    url(r"seach_sheng/$", views.seach_sheng, name="seach_sheng"),
    url(r"seach_shi/(\d+)$", views.seach_shi, name="seach_shi"),
    url(r"seach_xian/(\d+)$", views.seach_xian, name="seach_xian"),

    url(r"^",views.index,name="index"),
]