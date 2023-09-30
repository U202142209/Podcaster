# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: login.py
 @time: 2023/8/20 16:38
  '''
import warnings

from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from ..config.EmailService import EmailService
from ..config.IpService import GetIpClass
from ..models import QUser
from .api import setError, setSuccess

warnings.filterwarnings("ignore")

from ..config.RedisService import RedisService


# 发送邮箱颜验证码
def getemailcode(request):
    email = request.GET.get("email", "123")
    # print("输入的邮箱是；", email)
    # 判断输入的邮箱是否在redis中存在，存在则不发送验证码，否则发送验证码，并加入redis设置5分钟的过期时间
    if RedisService.get("haveSendCode" + email):
        # print("redis中存在了邮箱:", email)
        data_dict = {"status": False, "msg": f"已经向邮箱邮箱:{email}发送了验证码，五分钟内只能发送一次"}
    else:
        code = EmailService.sendVerificateCode(send_to=email)
        # print("向邮箱", email, "发送验证码成功：", code)
        if code:
            request.session["email"] = email
            request.session['email_login_code'] = code
            request.session.set_expiry(60 * 5)
            data_dict = {"status": True,
                         "msg": "成功向邮箱；" + email + "发送了验证码，请在5分钟内输入正确的验证码完成验证。"}
            # 将邮箱信息加入redis
            RedisService.set("haveSendCode" + email, email, 60 * 5)
        else:
            data_dict = {"status": False, "msg": "验证码发送失败，请检查邮箱是否合法或联系系统管理员解决"}
    return JsonResponse(data_dict)


class LoginView(View):
    """类视图：处理注册"""

    def get(self, request):
        if request.session.get('is_logined', ""):
            return redirect('/campus/')
        """处理GET请求，返回注册页面"""
        return render(request, "shopping_login.html", {"msg": " "})

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        if not request.session.get("email", None):
            return render(
                request, "shopping_login.html",
                {
                    "msg": "请点击获取邮箱验证码",
                    "email": request.POST.get("email", "")
                })
        code = request.POST.get("code", "")
        # print("code", code)
        # print(request.session.get("email_login_code", ""))
        if str(code) != str(request.session.get("email_login_code", "")):
            return render(
                request, "shopping_login.html",
                {
                    "msg": "输入的邮箱验证码不正确",
                    "email": request.session.get("email", "")
                }
            )
        curuser = QUser.objects.filter(
            email=request.session.get("email")
        ).first()
        if not curuser:
            curuser = QUser.objects.create(
                username=request.session.get("email"),
                email=request.session.get("email"),
                ip=GetIpClass.getIpFromRequest(request),
            )
        else:
            curuser.ip = GetIpClass.getIpFromRequest(request)
            curuser.save()
        request.session["is_logined"] = True
        request.session["email"] = curuser.email
        request.session["username"] = curuser.username
        # 三天免登录
        request.session.set_expiry(60 * 60 * 24 * 3)
        return redirect("/campus/")


def checkloginController(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("is_logined", ""):
            # 用户已登录，继续执行原函数
            return view_func(request, *args, **kwargs)
        else:
            # 用户未登录，跳转到登录页面
            return render(request, "shopping_login.html", {"msg": "无权访问，请先登录"})

    return wrapper


def checkloginRestController(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("is_logined", ""):
            # 用户已登录，继续执行原函数
            return view_func(request, *args, **kwargs)
        else:
            # 用户未登录，跳转到登录页面
            return setError(msg="无权访问，请先登录")

    return wrapper


from django.contrib.sessions.models import Session


def logout(request):
    return setSuccess(msg="ok", data={"count": Session.objects.all().delete()})
