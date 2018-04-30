#encoding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from hashlib import sha1
from models import *
import user_decorator
from df_goods.models import GoodsInfo
from df_cart.models import *
from django.db.models import Sum,Count

#注册
def register(request):
	# return HttpResponse('ok')
	return render(request,'df_user/register.html')

# 处理注册
def register_handle(request):
	# 接受表单数据
	post = request.POST
	uname = post.get('user_name')
	upwd = post.get('pwd')
	cpwd = post.get('cpwd')
	uemail = post.get('email')
	# 判断两次密码
	if upwd !=cpwd:
		return render(request,'df_user/register.html')
	# 密码加密
	s1 = sha1()
	s1.update(str(upwd))
	sha1_pwd = s1.hexdigest()
	# 创建对象
	user = UserInfo()
	user.uname = uname
	user.upwd = sha1_pwd
	user.uemail = uemail
	#存入数据库
	user.save()
	#注册成功,跳转至登陆页面
	return redirect('/user/login/')

# 检测用户是否存在
def name_exist(request):
	name = request.GET['name']
	count = UserInfo.objects.filter(uname=name).count()
	return JsonResponse({'data':count})

#登录页面
def login(request):
	return render(request,'df_user/login.html')
#处理登陆
def login_handle(request):
	# print(request.POST)
	name  = request.POST['username']
	pwd = request.POST['pwd']
	obj= UserInfo.objects.filter(uname=name)
	url = request.COOKIES.get('url','/')
	#如果用户存在,则进行密码验证
	if obj.count():
		obj = obj.values()[0]
		uname = obj['uname']
		upwd = obj['upwd']
		s1 = sha1()
		s1.update(str(pwd))
		pwd = s1.hexdigest()
		# 密码验证
		if name==uname and pwd==upwd:
			request.session['user_id'] = obj['id']
			request.session['uname'] = uname			
			#查询购物车数据
			request.session['cart_count'] = CartInfo.objects.values('count').aggregate(cart_count=Sum('count'))['cart_count']
			# request.session.set_expiry(0)
			context = {'name':name==uname,'pwd':pwd==upwd,'uname':uname,'url':url}
			# 设置cookie
			try:
				jr = JsonResponse(context)
				remenber=request.POST['remenber']
				jr.set_cookie("uname",uname)
			except Exception:
				jr.set_cookie("uname",'0',max_age=-1)
			finally:
				return jr			
		else:
			context={'name':1,'pwd':0,'url':url}
	else:
		context={'name':0,'pwd':0,'url':url}
	return JsonResponse(context)

@user_decorator.login
# 个人信息
def user_info(request):
	info = UserInfo.objects.get(id=request.session['user_id'])
	scan_ids = request.COOKIES.get('scan_ids','')
	scan_ids = scan_ids.split('_')
	print(scan_ids)
	scan_info = []
	if scan_ids != ['']:
		for each in scan_ids:
			each = each.split(',')
			scan_info.append((each[0],GoodsInfo.objects.get(pk=each[1])))
	context = {'uemail':info.uemail,'pageName':1,'title':'个人信息','scan_info':scan_info}
	print(scan_info)
	return render(request,'df_user/user_center_info.html',context)

# 全部订单
@user_decorator.login
def user_order(request):
	context={'pageName':1,'title':'全部订单'}
	return render(request,'df_user/user_center_order.html',context)
# 收货地址
@user_decorator.login
def user_site(request):
	info = UserInfo.objects.get(id=request.session['user_id'])
	# 添加到地址簿
	addr = UserAddress()
	warm = ''
	if request.method == 'POST':
		post = request.POST
		addr.ureceiver = post['ureceiver']
		addr.uaddress = post['uaddress']
		addr.upostcode = post['upostcode']
		addr.uphone = post['uphone']
		addr.user_id = info.id
		# 判断地址是否重复
		count = info.useraddress_set.filter(ureceiver=addr.ureceiver,uphone=addr.uphone,uaddress=addr.uaddress).count()		
		if count == 0:
			addr.save()
		else:
			warm = "<script type=\"text/javascript\">alert(\"数据已存在\")</script>"
	context={'addr':addr,'warm':warm,'pageName':1,'title':'收货地址'}
	return render(request,'df_user/user_center_site.html',context)

# 退出
def logout(request):

		# request.session.flush()
		# request.session.clear()
	try:
		del request.session['user_id']
		del request.session['uname']
			
	except Exception:
		pass

	finally:
		response = HttpResponseRedirect('/')
		response.delete_cookie('scan_ids')
		return response







