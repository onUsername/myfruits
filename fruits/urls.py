from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index/$', views.index, name="index"),
    url(r'^detail/(\d+)$', views.detail, name="detail"),
    url(r'^list/(\d+)/(\d+)$', views.list, name="list"),
    url(r'^add_car/$', views.add_car, name="add_car"),
    url(r'^get_count/$', views.get_count, name="get_count"),
    url(r'^check_car/$', views.check_car, name="check_car"),
    url(r'^up_car/$', views.up_car, name="up_car"),
    url(r'^del_car/$', views.del_car, name="del_car"),
    ]