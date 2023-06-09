from django.urls import re_path as url
from django.urls import re_path, path, include
from .view import index,detail

urlpatterns = [
    path("", index.shopping_index, name="shopping_index"),
    path("getDataApi/",index.getDataApi,name="getDataApi"),
    path("detail/",detail.detail,name="detail"),
    path("detail/getdataapi/",detail.detail_getdataapi),
    path("detail/getcommentapi/",detail.getCommentDataApi,name="getCommentDataApi"),
    path("addwatchnum/",detail.addWatchNum,name="addwatchnum"),

]
