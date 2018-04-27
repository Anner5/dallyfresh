from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'dallyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('df_user.urls',namespace='user')),
    url(r'^',include('df_goods.urls',namespace='goods')),
    url(r'^tinymce/', include('tinymce.urls')),
]
