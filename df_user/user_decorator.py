# coding=utf-8
from django.http import HttpResponseRedirect,JsonResponse
# 如果未登录则跳转到登录页面
def login(func):
	def login_func(requset,*args,**kwargs):
		if requset.session.has_key('user_id'):
			return func(requset,*args,**kwargs)
		else:
			red = HttpResponseRedirect('/user/login') #反向解析'user:login',args=()
			#requset.get_full_path获取包括关键字等
			# red.set_cookie('url',requset.get_full_path())
			return red
			# HttpResponseRedirect('/user/login')
	return login_func



