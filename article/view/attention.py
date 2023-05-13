from ..models import Attention
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect

def attention_list(request):
    attentions=Attention.objects.filter(
        guest_id = request.session.get('info').get('id')
    )
    return render(request,'attention_list.html',{"attentions":attentions ,"sum":len(attentions)})


# 取消关注
def attention_delete(request):
    host_id=request.GET.get("host_id")
    obj=Attention.objects.filter(
        host_id=host_id,
        guest_id=request.session.get('info').get('id')
    )
    if obj:
        obj.delete()
        return JsonResponse({"status":True})
    return JsonResponse({"status": False ,"error":"取消收藏失败，数据认证错误." })