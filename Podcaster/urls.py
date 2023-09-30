from django.conf import settings  ##新增
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path, path
from django.urls import re_path as url
from django.views import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('article.urls')),
    path('campus/', include('shoppingapp.urls')),

    # 静态资源路径
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# handler404 = views.page_not_found
# handler500 = views.server_error
# handler400 = views.bad_request
