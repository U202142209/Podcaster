from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .api import *
from ..config.getData import get_nid, getCurrentPage, getPageDividerString
import warnings

warnings.filterwarnings("ignore")


# /campus/?currentPage=0
from .login import checkloginController,checkloginRestController
@checkloginController
def shopping_index(request):
    currentPage = getCurrentPage(request.GET.get("currentPage"))
    pageDivideString = getPageDividerString(currentPage=currentPage)
    nid = get_nid()
    # shopping_home.html
    request.session["nidnidnid"] = nid
    return render(request, "shopping_index.html", {
        "currentPage": currentPage, "pageDivideString": pageDivideString, "nid": nid,
    })

@checkloginRestController
@csrf_exempt
# 获取帖子详细数据
def getDataApi(request):
    try:
        # 参数校验
        assert request.method == "POST", "此接口仅限于接受post请求"
        assert request.POST.get("nid") != None, "缺少必要参数"
        assert request.session.get("nidnidnid", "") == request.POST.get("nid"), "参数校验不正确"
        # 获取参数
        currentPage = getCurrentPage(request.POST.get("length"))
        # 判断是否输入了关键字
        keyword = request.POST.get("keyword", "")
        if keyword:
            result = search(keyword=keyword, currentPage=currentPage)
        else:
            curclassify = request.POST.get("curclassify", "")
            order = request.POST.get("order", "")
            result = getTieZi(currentPage=currentPage, radioGroup=curclassify, type=order)
        if result:
            return setSuccess(msg="ok", data=result)
        return setError(msg="没有数据了")
    except Exception as error:
        return setError(msg=f"{error},获取数据失败")

# 获取用户的详细信息
def getAllPostByOpenid(openid):
    data = []
    length = 0
    while 1:
        res = requests.get(
            url="https://www.yqtech.ltd:8802/gettaskbyOpenIdQuanzi",
            params={"openid": openid, "length": length}, verify=False).json()["taskList"]
        if len(res) == 0:
            return data
        length += 10
        data.extend(res)

@checkloginController
def getuserdetailpage(request):
    openid = request.GET.get("openid", "o7FW15WQQQakCpA12B2HhQ4GykGE")
    return render(request, "userdetail.html", {
        "openid": openid
    })


# 删除帖子
def deleteTiezi(pk="A6D78EC1D9F8250260563D34809847E1"):
    return requests.get(
        url=f"https://www.yqtech.ltd:8802/deleteTaskQuanzi?pk={pk}",
        verify=False
    )

@checkloginRestController
def deletepost(request):
    pwd = request.GET.get("pwd", "")
    if pwd != "wobushidalao1":
        return JsonResponse({"msg": "此密钥已失效"}, json_dumps_params={'ensure_ascii': False}, )
    res = deleteTiezi(pk=request.GET.get("pk", "")).json()
    try:
        data = {"msg": "失败", "data": res}
        if res["code"] == 200:
            data = {"msg": "操作成功！", "data": res}
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, )
    except:
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, )
