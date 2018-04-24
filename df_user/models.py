from django.db import models

class UserInfo(models.Model):
	uname = models.CharField(max_length=20,unique=True)
	upwd = models.CharField(max_length=40)
	uemail = models.CharField(max_length=30)
	isDelete = models.BooleanField(default=0)
	

class UserAddress(models.Model):
	ureceiver = models.CharField(max_length=20,default='')
	uaddress = models.CharField(max_length=100,default='')
	upostcode = models.CharField(max_length=6,default='')
	uphone = models.CharField(max_length=11,default='')
	isDelete = models.BooleanField(default=0)
	user = models.ForeignKey('UserInfo')
		
