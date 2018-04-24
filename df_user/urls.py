from django.conf.urls import url
import views

urlpatterns = [
	url(r'^register/$',views.register,name='register'),
	url(r'^register_handle/$',views.register_handle),
	url(r'^name_exist/$',views.name_exist),
	url(r'^login/$',views.login,name='login'),
	url(r'^login_handle/$',views.login_handle),
	url(r'^user_center_info/$',views.user_center_info),
	url(r'^user_center_order/$',views.user_center_order),
	url(r'^user_center_site/$',views.user_center_site),
]