# 网站对外共享api接口

from django.http import HttpResponse,JsonResponse    # 导入模块
from ..config import apiSebdEmailCode   # 发送验证码的函数
from ..config import send_message
from django.views.decorators.csrf import csrf_exempt    # 解除csrf_token的限制


@csrf_exempt
def sendemailcode(request):
    """提高服务门槛，仅限于post请求方式"""
    if request.method=="POST":
        email=request.POST.get('email')     # 获取email邮箱地址
        # 发送验证码
        return HttpResponse(apiSebdEmailCode(email))
    else:
        return HttpResponse("请求方式不正确，请使用post请求此地址。")

def getData(request):
    response={
        "status":True,
    }
    return JsonResponse(response)

@csrf_exempt
def sendemailmessage(request):
    if request.method=="POST":
        email=request.POST.get('email')     # 获取email邮箱地址
        message = request.POST.get('message')
        if send_message(
            email=email,
            message=message,
        ):
            return HttpResponse(f"成功向邮箱:{email} 发送了错误日志。")
        return HttpResponse("邮箱日志发送失败。")
    return HttpResponse("请求方式不正确，请使用post请求此地址。")