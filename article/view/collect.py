from django.shortcuts import render,HttpResponse,redirect
from ..models import Collect
from django.http import JsonResponse


def collect_list(request):
    collects=Collect.objects.filter(
        user_id=request.session['info']['id'],
    ).order_by('-create_time')
    return render(request,'collect_list.html',{"collects":collects , "sum":len(collects)})

def collect_delete(request):
    user_id=request.GET.get('user_id')
    article_id=request.GET.get('article_id')

    if user_id == str( request.session['info']['id'] ) :
        collect=Collect.objects.filter(user_id=user_id , article_id=article_id ).first()
        if collect:
            collect.delete()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": "数据匹配不成功。取消收藏失败"})
    return JsonResponse({"status":False , "error":"检测到不安全的请求，数据匹配不成功。"})
