from django.http import JsonResponse
from django.shortcuts import render
from ..config.getData import getAPageData, get_nid, getCurrentPage, getPageDividerString

def shopping_index(request):        # /shopping/?currentPage=0
    currentPage = getCurrentPage(request.GET.get("currentPage"))
    pageDivideString = getPageDividerString(currentPage=currentPage)
    nid = get_nid()
    request.session["nidnidnid"] = nid
    return render(request, "shopping_index.html", {
        "currentPage": currentPage, "pageDivideString": pageDivideString, "nid": nid,
    })

def getDataApi(request):            # /shopping/getDataApi/
    try:
        assert request.method == "POST", "此接口仅限于接受post请求"
        assert request.POST.get("nid") != None, "缺少必要参数"
        assert request.session.get("nidnidnid", "") == request.POST.get("nid"), "参数校验不正确"
        currentPage = getCurrentPage(request.POST.get("currentPage"))
        result = getAPageData(currentPage)
        request.session.clear()
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False}, )
    except Exception as error:
        return JsonResponse({
            "code": 404, "message": f"{error},获取数据失败",
        }, json_dumps_params={'ensure_ascii': False}, )

