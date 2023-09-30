from django.urls import re_path as url
from django.urls import re_path, path, include
from . import views
from .view import user, ajax, article, collect, attention, message,comment,api

urlpatterns = [
    url(r'^$', views.index, name="index"),  # 这里 r'^$' 里面得加上 ^$ 。如果里面还要配置 URL 结尾记的加上反斜杠，如 r'^index/$'
    path("register/", user.register, name="register"),
    # 获取邮箱验证码
    path('getemailcode/', ajax.getemailcode),
    path('login/', user.login, name="login"),
    path('random_img/', views.random_img),
    path("logout/", user.logout, name="logout"),
    path("console/", user.console, name="console"),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("console/article/list.html", article.article_list, name="article_list"),
    path("article_add/", article.article_add, name="article_add"),
    path('article/delete/', article.display_none),
    #
    path("article/", article.article),
    path("recycle_list/", article.recycle_list, name="recycle_list"),
    # 回收到草稿箱
    path("article_draft_list/", article.article_draft_list, name='article_draft_list'),
    path('article_recycle_to_draft/', article.article_recycle_to_draft, name="article_recycle_to_draft"),
    # 彻底删除博客
    path('article_delete_totally/', article.article_delete_totally, name="article_delete_totally"),
    path("article/change/<int:nid>", article.article_change, name='article_change'),

    # 收藏
    path('create/collect/', ajax.create_collect),
    path('collect/list/', collect.collect_list, name="collect_list"),
    path("collect/delete/", collect.collect_delete, name="collect_delete"),
    # 关注
    path('attention/list/', attention.attention_list, name="attention_list"),
    path("user/add/attention/", ajax.user_add_attention, name="user_add_attention"),
    path('attention/delete/', attention.attention_delete, name="attention_delete"),
    # 上传头像
    path('uploadtouxiang/', user.uploadtouxiang, name="uploadtouxiang"),
    path('user/', user.user_detail, name="user_detail"),
    path('message/list/', message.message_list, name='message_list'),
    path('message/delete/', message.message_delete),
    path('message/read', message.message_read, name="message_read"),
    path('message/to/read/', message.message_to_read, name="message_to_read"),
    path('message/to/not/read/', message.message_to_not_read),

    # 已有代码，处理一级回复
    path('post-comment/', comment.post_comment, name='post_comment'),
    path("comment/delete/",comment.comment_delete,name="comment_delete"),
    # 加载 更多
    path('show/more/hots/',views.get_more_hots,name="get_more_hots"),



    # 测试
    path('genres/', views.test_mptt),
    path("download/",views.download ,name="download"),
    path('search/',views.search ,name="search"),
    path("login/email/",user.emaillogin ,name="emaillogin"),
    path("'/setting/security/",user.setting_security ,name="setting_security"),


    # api接口
    path('api/sendemailcode/',api.sendemailcode ,name="sendemailcode"),
    path("getdata/",api.getData,name='getdata'),
    path('api/sendemailmessage/',api.sendemailmessage,name="sendemailmessage"),
    path('api/sendAllMessage/',api.sendAllMessage,name="sendAllMessage"),



]
