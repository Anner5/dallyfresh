# encoding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
def index(request):
	# 查询分类的最新4条/最热4条数据
	typelist = TypeInfo.objects.all() #取出所有分类名
	try:
		uname = request.session['uname']
	except Exception:
		uname = ''
	if len(typelist) > 5:
		type01 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
		type02 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
		type11 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
		type12 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
		type21 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
		type22 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
		type31 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
		type32 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
		type41 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
		type42 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
		type51 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
		type52 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
		context = {'titile':'首页','guset_cart':1,
					'type01':type01,'type02':type02,
					'type11':type11,'type12':type12,
					'type21':type21,'type22':type22,
					'type31':type31,'type32':type32,
					'type41':type41,'type42':type42,
					'type51':type51,'type52':type52,
					'uname':uname}
		return render(request,'df_goods/index.html',context)
	else:
		return render(request,'df_goods/index.html',{'uname':uname})
def goods_list(request,tid,pindex,sort):
	tid = int(tid)
	sort = int(sort)
	#升级排序
	switch = request.GET.get('switch')
	if switch=='':
		switch = '-'
	else:
		switch = ''
	if tid == 0:
		# 点击导航'全部分类' 按默认排序
		goods_list = GoodsInfo.objects.all().order_by(switch+'id')
		typeinfo = ''
	else:
		typeinfo = TypeInfo.objects.get(pk=tid)
		if sort == 3:		
			goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by(switch+'gclick')
		elif sort == 1:
			goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by(switch+'id')
		else:
			goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by(switch+'gprice')
	news = goods_list.order_by('-id')[0:2]
	paginator = Paginator(goods_list,10) #按10个/页进行分页
	page = paginator.page(int(pindex)) # 当前页所有对象
	context = {'pindex':pindex,
				'guset_cart':1,
				'page':page,
				'paginator': paginator,
				'typeinfo': typeinfo,
				'sort': sort,
				'news': news,
				'title':'商品列表',
				'switch':switch}

	return render(request,'df_goods/list.html',context)

def detail(request,tid,gid):
	typeinfo = TypeInfo.objects.get(pk=int(tid))
	news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
	goodsinfo = GoodsInfo.objects.get(pk=int(gid))
	# 点击量增加一次
	goodsinfo.gclick += 1
	goodsinfo.save()
	context = {'typeinfo':typeinfo,
				'detail':1,
				'goodsinfo':goodsinfo,
				'news':news}
	return render(request,'df_goods/detail.html',context)