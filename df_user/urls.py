from django.conf.urls import url
import views

urlpatterns = [
	url(r'^register/$',views.register,name='register'),
	url(r'^register_handle/$',views.register_handle),
	url(r'^name_exist/$',views.name_exist),
	url(r'^login/$',views.login,name='login'),
	url(r'^login_handle/$',views.login_handle),
	url(r'^info/$',views.user_info,name='info'),
	url(r'^order/$',views.user_order,name='order'),
	url(r'^site/$',views.user_site,name='site'),
	url(r'^logout/$',views.logout,name='logout'),
]