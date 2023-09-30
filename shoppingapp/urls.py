from django.urls import re_path as url
from django.urls import re_path, path, include
from .view import index, detail, user, login

urlpatterns = [
    # 首页
    path("", index.shopping_index, name="shopping_index"),
    # 获取帖子数据
    path("getDataApi/", index.getDataApi, name="getDataApi"),
    # 帖子详情页
    path("detail/", detail.detail, name="detail"),
    # 获取帖子详细数据
    path("detail/getdataapi/", detail.detail_getdataapi),
    # 获取帖子评论数据
    path("detail/getcommentapi/", detail.getCommentDataApi, name="getCommentDataApi"),
    path("addwatchnum/", detail.addWatchNum, name="addwatchnum"),
    path("getuserdetailpage", index.getuserdetailpage, name="getuserdetailpage"),
    # 删除帖子
    path("deletepost/", index.deletepost, name="deletepost"),

    # 用户中心
    path("userdetail/", user.userdetail, name="userdetail"),
    path("userPost/", user.userPost, name="userPost"),
    path("login/", login.LoginView.as_view(), name="slogin"),
    path("getemailcode/", login.getemailcode, name="shoppinggetemailcode"),
    # 退出登录：logout
    path("logout/", login.logout, name="logout"),
]
