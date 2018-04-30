# encoding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator

def index(request):
	# 查询分类的最新4条/最热4条数据
	typelist = TypeInfo.objects.all() #取出所有分类名
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
		context = {'title':'首页','guest_cart':1,
					'type01':type01,'type02':type02,
					'type11':type11,'type12':type12,
					'type21':type21,'type22':type22,
					'type31':type31,'type32':type32,
					'type41':type41,'type42':type42,
					'type51':type51,'type52':type52,
					}
		return render(request,'df_goods/index.html',context)
	else:
		return render(request,'df_goods/index.html')
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
				'guest_cart':1,
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

	context = {'title':'商品详情',
				'typeinfo':typeinfo,
				'detail':1,
				'goodsinfo':goodsinfo,
				'news':news,
				'guest_cart':1}
	response = render(request,'df_goods/detail.html',context)
	# 记录最近浏览量,在用户中心使用
	scan_ids = request.COOKIES.get('scan_ids','')
	scan_ids = scan_ids.split('_')
	if scan_ids != ['']:
		for each in scan_ids[:]:
			if gid in each.split(',')[1]:
				scan_ids.remove(each)			
		scan_ids.insert(0,'%s,%s' % (tid,gid))
	else:
		scan_ids = []
		scan_ids.insert(0,'%s,%s' % (tid,gid))

	if len(scan_ids) > 5:
		del scan_ids[5:]	
	scan_ids = '_'.join(scan_ids)		
	response.set_cookie('scan_ids',scan_ids)

	# goods_id = '%d' % tid #格式化
	# if goods_ids != '':
	# 	goods_ids1 = goods_ids.split(',') #分割成列表
	# 	if goods_id in goods_ids1: #goods_ids1.count(goods_id) > 0
	# 		goods_ids1.remove(goods_id)
	# 	goods_ids1.insert(0,goods_id)
	# 	if len(goods_ids1) > 5: #超过5个去掉最后一个
	# 		# del goods_ids1[5]
	# 		goods_ids1.pop()
	# 	goods_ids = ','.join(goods_ids1)
	# 	print(goods_ids)
	# else:
	# 	goods_ids = goods_id #如果浏览器记录为空,则直接添加
	# # 写入cookie
	# response.set_cookie('goods_ids',goods_ids)
	return response