import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..config.getData import getAPageData, get_nid, getCurrentPage, getPageDividerString
import threading


def detail(request):
    article_id = request.GET.get("id")
    if not article_id:
        redirect("/shopping")
    return render(request, "detail.html", {
        "article_id": article_id,
    })


import requests


def detail_getdataapi(request):
    return JsonResponse(
        requests.get(
            url="https://www.yqtech.ltd:8802/gettaskbyIdQuanzi?pk=" + str(request.GET.get("pk")),
        ).json(),
        json_dumps_params={'ensure_ascii': False},
    )


def getCommentDataApi(request):
    return JsonResponse(
        requests.get(
            url="https://www.yqtech.ltd:8802/getCommentByTypeQuanzi?length=0&pk=" + str(
                request.GET.get("pk")) + "&type=0",
        ).json(),
        json_dumps_params={'ensure_ascii': False},
    )


def visit(pk, num):
    url2 = "https://www.yqtech.ltd:8802/gettaskbyIdQuanzi?pk=" + pk
    url3 = "https://www.yqtech.ltd:8802/getCommentByTypeQuanzi?length=0&pk=" + pk + "&type=0"
    for i in range(num):
        res = requests.get(url2).status_code
        res = requests.get(url3).status_code


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
        assert pk!=None ,"输入的id不能为空"
        assert pwd == "admin" ,"密钥输入不正确，无法执行此操作。"
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

