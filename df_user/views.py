#encoding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from hashlib import sha1
from models import *

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
	name  = request.POST['username']
	obj= UserInfo.objects.filter(uname=name)
	#如果用户存在,则进行密码验证
	if obj.count():
		obj = obj.values()[0]
		uname = obj['uname']
		upwd = obj['upwd']
		pwd = request.POST['pwd']
		s1 = sha1()
		s1.update(str(pwd))
		pwd = s1.hexdigest()
		request.session['user_id'] = obj['id']
		request.session['uname'] = uname
		context={'name':name==uname,'pwd':pwd==upwd}
	else:
		context={'name':0,'pwd':0}
	return JsonResponse(context)
# 个人信息
def user_center_info(request):
	info = UserInfo.objects.get(id=request.session['user_id'])
	context = {'uname':info.uname,'uemail':info.uemail}
	return render(request,'df_user/user_center_info.html',context)
# 订单
def user_center_order(request):
	context={'uname':request.session['uname']}
	return render(request,'df_user/user_center_order.html',context)
# 收货地址
def user_center_site(request):
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
		context={'addr':addr,'uname':info.uname,'warm':warm}
		return render(request,'df_user/user_center_site.html',context)
	





