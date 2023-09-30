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

flag=False
from ..models import User
def sendAllMessage(request):
    global flag
    if flag:
        return HttpResponse("只能执行一次")
    # users=User.objects.filter()
    users=User.objects.filter(email__contains="2869210303")
    print(len(users))
    for user in users:
        print(user.email)
        message="【重要通知】各位博客小伙伴们，大家好。本站（http://43.138.46.106:8001/）即将推出新功能（例如用户之间的私信，聊天、发布下载资源等（仿CSDN）），如果您对此网站有何期待，或者有哪些新奇的想法，欢迎在本帖子的下面留言。http://43.138.46.106:8001/article/?nid=202306100022459182      新功能正在研发中！敬请期待."
        res= send_message(
            email=user.email,
            message=message,
        )
        print(user.email,res)
    flag=True

    return HttpResponse("sendAllMessage is called.")