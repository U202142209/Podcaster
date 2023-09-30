# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: user.py
 @time: 2023/8/14 7:54
  '''
from .api import *
from .index import getAllPostByOpenid
from .login import checkloginRestController
from ..config.getData import getCurrentPage


@checkloginRestController
def userdetail(request):
    openid = request.POST.get("openid", "")
    d = getAllPostByOpenid(openid=openid)
    data = {"data": d, "len": len(d), }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, )


# 用户发布的
@checkloginRestController
def userPost(request):
    try:
        openid = request.GET.get("openid", "")
        type = request.GET.get("type", "")
        currentPage = getCurrentPage(request.GET.get("length", ""))
        print(openid, currentPage, type)
        assert openid and type, "parameter error"
        if type == "tiezi":
            res = getTieZiByOpenid(openid=openid, length=currentPage)
        elif type == "comment":
            res = getCommentsByOpenid(openid=openid, length=currentPage)
        elif type == "message":
            res = getMessageByOpenid(openid=openid, length=currentPage)
        else:
            raise Exception("parameter error 2")
        return setSuccess(msg="ok", data=res)
    except Exception as error:
        import traceback
        traceback.print_exc()
        return setError(str(error))


# 用户喜欢的
def userLike(request):
    return


# 用户评论的
def userComment(request):
    return


# 用户的消息
def userMessage(request):
    return
