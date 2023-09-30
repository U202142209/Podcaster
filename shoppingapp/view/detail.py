import threading

from django.shortcuts import render, redirect

from .api import *
from .login import checkloginController, checkloginRestController


@checkloginController
def detail(request):
    article_id = request.GET.get("id")
    if not article_id:
        redirect("/campus")
    return render(request, "detail.html", {
        "article_id": article_id,
    })


# 获取帖子详情
@checkloginRestController
def detail_getdataapi(request):
    res = getTieZiDetail(pk=request.GET.get("pk", ""))
    if res:
        return setSuccess(msg="ok", data=res)
    return setError("此帖子不存在或者已被删除，无法查看")


# 获取评论数据
@checkloginRestController
def getCommentDataApi(request):
    try:
        data = []
        length = 0
        for i in range(10):
            r = requests.get(
                url="https://www.yqtech.ltd:8802/getCommentByTypeQuanzi",
                params={
                    "type": 0,
                    "length": length,
                    "pk": request.GET.get("pk", ""),
                }
            ).json()
            if r["commentList"]:
                data.extend(r["commentList"])
                length += 10
            else:
                break
        return setSuccess(msg="ok", data=data)
    except:
        import traceback
        traceback.print_exc()
        return setError(msg="没有数据")


def visit(pk, num):
    url2 = "https://www.yqtech.ltd:8802/gettaskbyIdQuanzi?pk=" + pk
    url3 = "https://www.yqtech.ltd:8802/getCommentByTypeQuanzi?length=0&pk=" + pk + "&type=0"
    for i in range(num):
        res = requests.get(url2).status_code
        res = requests.get(url3).status_code

@checkloginController
def addWatchNum(request):
    if request.method == "GET":
        return render(request, "addWatchNum.html", {
            "message": "",
        })
    pk = request.POST.get("pk")
    try:
        num = int(request.POST.get("num"))
    except:
        num = 10
    try:
        pwd = request.POST.get("pwd")
        assert pk != None, "输入的id不能为空"
        assert pwd == "admin", "密钥输入不正确，无法执行此操作。"
        threading.Thread(target=visit, args=(
            pk,
            num,
        )).start()
        return render(request, "addWatchNum.html", {
            "message": "任务已加入队列，请等待执行结果...",
        })
    except Exception as error:
        return render(request, "addWatchNum.html", {
            "message": error,
        })
