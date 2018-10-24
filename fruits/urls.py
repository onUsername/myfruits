from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index/$', views.index, name="index"),
    url(r'^detail/(\d+)$', views.detail, name="detail"),
    url(r'^list/(\d+)/(\d+)$', views.list, name="list"),
    url(r'^add_car/$', views.add_car, name="add_car"),
    ]