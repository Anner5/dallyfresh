# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from df_user import user_decorator
from models import *
from df_goods.models import *
from df_user.models import *
from django.db.models import Count,Sum

# 购物车页面
@user_decorator.login
def cart(request):
	# 从数据库读取购物车商品信息
	uid = request.session.get('user_id')
	# 读取购物车商品id
	carts = CartInfo.objects.filter(user_id=uid)
	context = {'title':'购物车',
			   'page_name':1,
			   'carts':carts}
	return render(request,'df_cart/cart.html',context)
	# count_list = carts.values('count')
	# goods_num = count_list.aggregate(goods_num=Sum('count'))['goods_num']
	# goods_num = goods_num if goods_num else 0
	# goods_ids = carts.values('goods_id')
	# goods_list = [] 	
	# for each in goods_ids:
	# 	goods_list.append(GoodsInfo.objects.get(id=each['goods_id']))

	# # count_list = GoodsInfo.objects.filter(id__in=goods_list)
	# cart_list = zip(goods_list,count_list)
	# print(cart_list)
	# context = {'title':'我的购物车','cart_list':cart_list,'goods_num':goods_num}
	# return render(request,'df_cart/cart.html',context)

# 添加商品到购物车
@user_decorator.login
def adds(request,gid,count):
	print('adds')
	uid = request.session.get('user_id')
	count = int(count)
	total = request.session['cart_count']
	#我的购物车显示的数量
	num = count + total if total != None else 0
	request.session['cart_count'] = num
	carts= CartInfo.objects.filter(user_id=uid,goods_id=gid)
	# 如果商品已在购物车,则只增加数量
	if len(carts):
		cart = carts[0]
		cart.count += count
	else:
		cart = CartInfo()
		cart.user_id = uid
		cart.goods_id = gid
		cart.count = count
	cart.save()
	if request.is_ajax():
		response = JsonResponse({"count":str(num)})
		return response
	return redirect('/user/cart/')

# 修改商品
@user_decorator.login
def edit(request,cart_id,count):
	count = int(count)
	cart_int = int(cart_id)	
	# 购物车商品数量调整
	total = request.session.get('cart_count',None)
	request.session['cart_count'] = count + total if total != None else 0
	
	# 修改购物车数据库
	# cart = CartInfo.objects.get(id=cart_id)
	# count1 = cart.count = count
	# cart.save()
	# data={'ok':0}
	try:
		cart = CartInfo.objects.get(id=cart_id)
		count1 = cart.count = count
		cart.save()
		data={'ok':0}
	except Exception:
		data = {'ok':count}
		print('false')
	print(data)
	return JsonResponse(data)
#删除商品
@user_decorator.login
def delete(request,cart_id):
	try:
		cart = CartInfo.objects.get(pk=int(cart_id))
		cart.delete()
		data = {'ok':1}
	except Exception:
		data = {'ok':0}
	return JsonResponse(data)
	# obj = CartInfo.objects.filter(goods_id=gid)
	# if count:
	# 	obj.update(count=count)
	# else:
	# 	obj.delete() #count=0,则物理删除
	# response = JsonResponse()
	# return response



