import datetime as dt
import threading  # 实验线程发送消息，提高效率，减少用户等待时间

from django.shortcuts import render, redirect

from ..config import get_ip, send_message, get_now_time
from ..forms import RegisterModelForm, LoginForm, SettingsModelForm, TouxiangChangeModelForm, EmailLoginForm, \
    SecurityModelForm
from ..models import *


# 用户注册
def register(reqtest):
    if reqtest.method == 'GET':
        if reqtest.session.get('info'):  # 如果已经登录，直接跳转到控制台
            return redirect('/console/')

        form = RegisterModelForm()
        return render(reqtest, 'register.html', {"form": form})
    form = RegisterModelForm(data=reqtest.POST)
    if form.is_valid():
        # 判断验证码是否正确
        if form.cleaned_data["code"] != reqtest.session.get("email_code", ""):
            form.add_error('code', "验证码输入错误")
            return render(reqtest, 'register.html', {"form": form})
        if form.cleaned_data['password'] != form.cleaned_data["conform_password"]:
            form.add_error("conform_password", "两次输入的密码不一致")
            return render(reqtest, 'register.html', {"form": form})
        # 判断用户名是否存在
        txt_username = form.cleaned_data['username']
        exists = User.objects.filter(username=txt_username).exists()
        if exists:
            form.add_error('username', "该用户名已经存在")
            return render(reqtest, 'register.html', {"form": form})
        form.instance.ip = get_ip(reqtest)
        form.save()
        return redirect("/login/?message=注册成功！请登录")
    return render(reqtest, 'register.html', {"form": form})


# 用户登录
def login(request):
    if request.method == "GET":
        if request.session.get('info'):  # 如果已经登录，直接跳转到控制台
            return redirect('/console/')

        message = request.GET.get("message")
        form = LoginForm()
        return render(request, 'login.html', {"form": form, "message": message})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get("image_code", "")
        print('正确的code;', code)
        if user_input_code != code:
            form.add_error('code', "验证码输入错误")
            return render(request, 'login.html', {"form": form})

        # 按照用户名 密码查询
        admin_object = User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 按照邮箱 ，密码查询
            admin_object = User.objects.filter(
                email=form.cleaned_data['username'], password=form.cleaned_data['password'],
            ).first()
            if not admin_object:
                form.add_error('password', "用户名或密码不正确")
                return render(request, 'login.html', {"form": form})
        request.session["info"] = {
            "id": admin_object.id,
            "username": admin_object.username,
            "touxiang": admin_object.touxiang.url
        }
        request.session["email"] = admin_object.email
        request.session["touxiang_changed"] = False

        request.session.set_expiry(60 * 60 * 24 * 3)
        # 更新用户的IP信息
        admin_object.ip = get_ip(request)
        admin_object.save()

        # 登录成功，消息提醒
        Message.objects.create(
            sender_id=request.session.get('info').get('id'),
            receiver_id=request.session.get('info').get('id'),
            content="  系统日志提醒，登录成功！登录时间 ；" + get_now_time(),
        )

        # 邮箱提醒

        msg = "你于 " + str(
            dt.datetime.now().strftime('%F %T')) + " 在[好记性博客共享平台]登录成功。登录账号；" + admin_object.username + "。登录ip；" \
              + get_ip(request) + "。 如非本人操作，请注意数据安全。"
        thread = threading.Thread(target=send_message, args=(request.session.get('email'), msg))
        thread.start()  # 启动线程

        return redirect('/console/?message=登录成功！')
    return render(request, 'login.html', {"form": form})


# 邮箱登录
def emaillogin(request):
    if request.method == "GET":
        if request.session.get('info'):  # 如果已经登录，直接跳转到控制台
            return redirect('/console/')

        form = EmailLoginForm()
        return render(request, 'emaillogin.html', {
            "form": form
        })

    form = EmailLoginForm(data=request.POST)
    if form.is_valid():

        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get("email_login_code", "")
        print('正确的code;', code)
        if user_input_code != code:
            form.add_error('code', "验证码输入错误")
            return render(request, 'emaillogin.html', {"form": form})

        admin_object = User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('code', "邮箱与验证码不匹配")
            return render(request, 'emaillogin.html', {"form": form})

        request.session["info"] = {
            "id": admin_object.id,
            "username": admin_object.username,
            "touxiang": admin_object.touxiang.url
        }
        request.session["email"] = admin_object.email
        request.session["touxiang_changed"] = False

        request.session.set_expiry(60 * 60 * 24 * 3)
        # 更新用户的IP信息
        admin_object.ip = get_ip(request)
        admin_object.save()

        # 登录成功，消息提醒
        Message.objects.create(
            sender_id=request.session.get('info').get('id'),
            receiver_id=request.session.get('info').get('id'),
            content="  系统日志提醒，登录成功！登录时间 ；" + get_now_time(),
        )

        # 邮箱提醒

        msg = "你于 " + str(
            dt.datetime.now().strftime('%F %T')) + " 在[好记性博客共享平台]登录成功。登录账号；" + admin_object.username + "。登录ip；" \
              + get_ip(request) + "。 如非本人操作，请注意数据安全。"
        thread = threading.Thread(target=send_message, args=(request.session.get('email'), msg))
        thread.start()  # 启动线程

        return redirect('/console/?message=登录成功！')
    return render(request, 'emaillogin.html', {"form": form})


# 退出登录
def logout(request):
    Message.objects.create(
        sender_id=request.session.get('info').get('id'),
        receiver_id=request.session.get('info').get('id'),
        content="  系统日志提醒，退出登录成功！ 退出登录时间；" + get_now_time(),
    )
    request.session.clear()
    return redirect("/login/?message=退出登录成功！")


# 控制台
def console(request):
    message = request.GET.get("message")
    try:
        user = User.objects.filter(id=request.session.get('info').get('id')).first()
    except:
        return redirect("/login?message=你还没有登录，无权访问。")
    txform = TouxiangChangeModelForm(instance=user)

    if request.method == 'GET':
        form = SettingsModelForm(instance=user)
        return render(request, 'console.html', {
            "user": user,
            "form": form,
            "message": message,
            "txform": txform,
        })
    form = SettingsModelForm(data=request.POST, instance=user)
    if form.is_valid():
        form.save()
        # 修改session
        request.session["info"] = {
            "id": form.instance.id,
            "username": form.instance.username,
            "touxiang": form.instance.touxiang.url
        }

        return redirect('/console/?message=更改设置成功!')
    return redirect('/console/?message=更改设置失败!')


# 更换头像
def uploadtouxiang(request):
    user = User.objects.filter(id=request.session.get('info').get('id')).first()
    txform = TouxiangChangeModelForm(data=request.POST, files=request.FILES, instance=user)

    if txform.is_valid():
        if request.session.get("touxiang_changed"):
            return redirect('/console/?message=更改头像失败，一段时间内只能更改一次!')
        txform.save()
        # 修改session数据
        request.session["info"] = {
            "id": txform.instance.id,
            "username": txform.instance.username,
            "touxiang": txform.instance.touxiang.url
        }
        request.session["touxiang_changed"] = True

        return redirect('/console/?message=更改头像成功!')
    return redirect('/console/?message=更改头像失败!')


# 用户详情页面
def user_detail(request):
    id = request.GET.get('id')
    if request.session.get('info'):
        if id == str(request.session.get('info').get('id')):
            return redirect('/console/')

    user = User.objects.filter(id=id, ).first()
    if user:
        articles = Article.objects.filter(
            author_id=id,
            display=True,
            publlic=True,
            status=True,
        ).order_by('-create_time')
        return render(request, 'user_detail.html', {
            "user": user,
            "articles": articles,
        })
    return render(request, '404.html')


# 安全设置
def setting_security(request):
    user = User.objects.filter(
        id=request.session.get('info').get('id'),
    ).first()
    if request.method == "GET":
        form = SecurityModelForm()
        return render(request, 'setting_security.html', {
            "form": form
        })

    form = SecurityModelForm(data=request.POST,instance=user)
    if form.is_valid():
        input_code = form.cleaned_data['code']
        change_password_code = request.session.get('change_password_code', "")
        if input_code != change_password_code:
            form.add_error('code', "验证码输入错误")
            return render(request, 'setting_security.html', {
                "form": form
            })
        form.save()         # BAOCUN mima
        return redirect('/console/?message="密码修改成功！"')
    return render(request, 'setting_security.html', {"form": form})
