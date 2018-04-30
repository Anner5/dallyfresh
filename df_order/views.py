# coding=utf-8
from django.shortcuts import render
from df_user import user_decorator

@user_decorator.login
def order(request):
	context = {'title':'提交订单','orderName':1,}
	return render(request,'df_order/place_order.html',context)