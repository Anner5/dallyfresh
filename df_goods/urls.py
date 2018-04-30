# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^list(\d+)_(\d+)_(\d+)/$',views.goods_list,name='goods_list'),
	url(r'^(\d+)_(\d+)/$',views.detail),
]
