from django.http import JsonResponse

from ..config import main, send_message
from ..models import *
import threading


def getemailcode(request):
    login=request.GET.get('login')
    changepwd=request.GET.get('changepwd')

    email = request.GET.get("email")
    print("输入的邮箱是；", email)

    # 判断是否是在注册式发送的验证码或者有邮箱登录时候的验证码
    if login:
        if not User.objects.filter(email=email).exists():
            return JsonResponse( {"status":False ,"msg":"此邮箱没有在本站注册，无法发送验证码。" })
        code = main(email)
        if code:
            request.session['email_login_code'] = code
            request.session.set_expiry(60 * 5)
            data_dict = {"status": True, "msg": "成功向邮箱；" + email + "发送了验证码，请在5分钟内输入正确的验证码完成验证。"}
        else:
            data_dict = {"status": False, "msg": "验证码发送失败，请确认 " + email + " 是否为有效的邮箱地址"}
        return JsonResponse(data_dict)


    if changepwd:
        # 修 改 密 码
        if not request.session.get('info'):
            return JsonResponse({"status": False, "msg": "Error;未登录,无法发送验证码。"})

        if not User.objects.filter(email=request.session.get("email","")).exists():
            return JsonResponse( {"status":False ,"msg":"Error;无法发送验证码。" })

        code = main(email)
        if code:
            request.session['change_password_code'] = code

            data_dict = {"status": True, "msg": "成功向邮箱；" + email + "发送了验证码，请在5分钟内输入正确的验证码完成验证。"}
        else:
            data_dict = {"status": False, "msg": "验证码发送失败，请确认 " + email + " 是否为有效的邮箱地址"}
        return JsonResponse(data_dict)



    if User.objects.filter(email=email).exists():
        data_dict = {"status": False, "msg": "邮箱；" + email + "已经注册成功了，一个邮箱只能注册一个账号。"}
        return JsonResponse(data_dict)
    code = main(email)
    if code:
        request.session["email_code"] = code
        request.session.set_expiry(60 * 5)
        data_dict = {"status": True, "msg": "成功向邮箱；" + email + "发送了验证码，请在5分钟内输入正确的验证码完成验证。"}
    else:
        data_dict = {"status": False, "msg": "验证码发送失败，请确认 " + email + " 是否为有效的邮箱地址"}
    print(code)
    return JsonResponse(data_dict)


def create_collect(request):
    id = request.GET.get("nid")
    if request.session.get("info"):
        if not Article.objects.filter(id=id, status=1, display=True, ).first():
            return JsonResponse({"status": False, "error": "该博客不存在,或者没有被博主公开，无法收藏"})
        if Collect.objects.filter(user_id=request.session['info']['id'], article_id=id, ).first():
            return JsonResponse({"status": False, "error": "已经收藏了该博客，无法重复收藏"})
        Collect.objects.create(
            user_id=request.session.get("info").get("id"),
            article_id=id,
        )
        # 发送消息
        article = Article.objects.filter(id=id).values('nid', "title", "author_id").first()  # 获取对应的文章
        author_username = User.objects.filter(id=article["author_id"]).values("username").first()["username"]
        string = '<a target="_blank" href="/article/?nid=' + article["nid"] + '"> ' + article["title"] + ' </a>'
        bozhu = '<a target="_blank" href="/user/?id=' + str(article["author_id"]) + '"> ' + author_username + ' </a>'
        Message.objects.create(
            receiver_id=request.session.get("info").get("id"),
            sender_id=article["author_id"],
            content="  提醒 ； 成功收藏了博主 " + bozhu + " 的博客 " + string
        )
        Message.objects.create(
            receiver_id=article["author_id"],
            sender_id=request.session.get("info").get("id"),
            content=" 成功收藏了 你 的博客 " + string,
        )

        # 邮箱提醒 ，
        article = Article.objects.filter(id=id).first()  # 获取对应的文章
        if article.author.love_remain:
            # 检查是否允许发送邮箱消息
            msg = " 用户 " + request.session.get('info').get('username') + "(http://101.43.229.177/user/?id=" + str(
                request.session.get('info').get(
                    'id')) + ") 收藏了你的博客 " + article.title + " (http://101.43.229.177/article/?nid=" + str(
                article.nid) + "). "
            thread = threading.Thread(target=send_message, args=(article.author.email, msg))
            thread.start()  # 启动线程

        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "无权操作，请先登录"})


# 关注博主
def user_add_attention(request):
    if not request.session.get('info'):
        return JsonResponse({"status": False, "error": "关注失败，请先登录！"})
    author_id = request.GET.get('author_id')

    if author_id == str(request.session.get('info').get('id')):
        return JsonResponse({"status": False, "error": "关注失败，无法关注自己！"})

    if Attention.objects.filter(host_id=author_id, guest_id=request.session.get('info').get('id'), ).exists():
        return JsonResponse({"status": False, "error": "你已经关注了该播主，无法重复关注。"})

    Attention.objects.create(host_id=author_id, guest_id=request.session.get('info').get('id'), )
    author_username = User.objects.filter(id=author_id).values("username").first()["username"]
    bozhu = '<a target="_blank" href="/user/?id=' + str(author_id) + '"> ' + author_username + ' </a>'
    Message.objects.create(
        receiver_id=request.session.get("info").get("id"),
        sender_id=author_id,
        content=" 平台提醒；你成功关注了了博主 " + bozhu
    )
    # 获取发起请求的用户名
    user_username = request.session.get("info").get("username")
    # 拼接html字符串
    user_detail = '<a target="_blank" href="/user/?id=' + str(
        request.session.get("info").get("id")) + '"> ' + user_username + ' </a>'
    Message.objects.create(
        receiver_id=author_id,
        sender_id=request.session.get("info").get("id"),
        content=" 平台提醒；" + user_detail + "关注了 你。"
    )

    # 发送邮箱提醒
    user = User.objects.filter(id=author_id).first()
    if user.attention_remain:
        # 检查是否允许发送邮箱消息
        msg = " 用户 %s (%s)关注了你。" % (request.session.get("info").get("username"),
                                    "http://101.43.229.177/user/?id=" + str(request.session.get("info").get("id")))
        thread = threading.Thread(target=send_message, args=(user.email, msg))
        thread.start()  # 启动线程

    return JsonResponse({"status": True})

