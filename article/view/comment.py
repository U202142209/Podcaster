import threading  # 线程模块

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..config import send_message, get_now_time  # 法如发送邮箱信息的模块
from ..models import Comment, Article, User, Message


# 新增参数 parent_comment_id
@csrf_exempt
def post_comment(request):
    if request.method == "GET":
        return JsonResponse({"status": False, "error": "评论失败，请求方式不正确。"})

    if not request.session.get("info"):
        return JsonResponse({"status": False, "error": "评论失败，请先登录。"})

    article_nid = request.POST.get("article_nid")

    article = Article.objects.filter(nid=article_nid, ).first()
    if not article:
        return JsonResponse({"status": False, "error": "数据错误，文章不存在。"})

    reply_to_id = request.POST.get("reply_to_id")
    reply_to_username = request.POST.get("reply_to_username")

    # 检测用户是否修改了数据
    if reply_to_id and reply_to_username:
        if not User.objects.filter(id=reply_to_id, username=reply_to_username):
            return JsonResponse({"status": False, "error": "数据错误，评论失败。"})

    parent_comment_id = request.POST.get("parent_comment_id")
    content = request.POST.get("content")
    sender_id = request.session.get("info").get("id")

    print("parent_comment_id;", parent_comment_id)
    print("reply_to_username;", reply_to_username)
    print("reply_to_id;", reply_to_id)
    print("content;", content)
    print("sender_id;", sender_id)

    new_comment = Comment(
        reply_to_id=reply_to_id,
        sender_id=sender_id,
        content=content,
        parent_id=parent_comment_id,
        article_id=article.id,
    )

    # 存在这个参数，说明时二级评论
    if parent_comment_id:
        parent_comment = Comment.objects.filter(id=parent_comment_id).first()
        if not parent_comment:
            return JsonResponse({"status": False, "error": "数据错误，评论失败。"})

        new_comment.parent_id = parent_comment.get_root().id
        # 被回复人
        # new_comment.reply_to = parent_comment.reply_to

        # 消息提醒 ， 如果时自己的评论，则不需要发送消息
        if not parent_comment.sender_id == sender_id:
            string = '<a target="_blank" href="/article/?nid=' + article.nid + '"> ' + "查看详情" + ' </a>'
            msg = Message.objects.create(
                sender_id=sender_id,
                receiver_id=new_comment.reply_to_id,
                comment_id=new_comment.id,
                content='回复了你的评论 ' + parent_comment.content + '。 回复内容；' + new_comment.content + '  去' + string
            )

            # 发送邮箱提醒
            if msg.receiver.message_remain:
                # 首先判断是否具有发送邮箱的权限
                ms = "用户 %s(%s) 回复了你的评论 %s 、回复内容；%s 、回复时间；%s ,点击链接(%s)，去查看详情吧！" % (
                    request.session.get('info').get('username'),
                    "http://101.43.229.177/user/?id=" + str(request.session.get('info').get('id')),
                    parent_comment.content,
                    new_comment.content,
                    get_now_time(),
                    "http://101.43.229.177/article/?nid=" + article.nid,
                )
                thread = threading.Thread(target=send_message, args=(msg.receiver.email, ms))
                thread.start()  # 启动线程

    else:
        # 这是首条评论
        print(type(sender_id))  # <class 'int'>
        print(type(article.author_id))  # <class 'int'>
        if not article.author_id == sender_id:

            # 自己在自己的文章下面评论无需提示
            string = '<a target="_blank" href="/article/?nid=' + article.nid + '"> ' + article.title + ' </a>'
            Message.objects.create(
                sender_id=sender_id,
                receiver_id=article.author_id,
                content=" 在你的博客 " + string + " 下面留言； " + new_comment.content,
                comment_id=new_comment.id
            )

            # 发送邮箱提醒
            if article.author.message_remain:
                # 首先判断是否具有发送邮箱的权限
                msg = "  用户 %s (%s) 在你的博客 %s(%s) 下面给你留言；%s  。留言时间;%s。 点击博客链接，去查看详情吧。" % (
                    request.session.get('info').get('username'),
                    "http://101.43.229.177/user/?id=" + str(request.session.get('info').get('id')),
                    article.title,
                    "http://101.43.229.177/article/?nid=" + article.nid,
                    new_comment.content,
                    get_now_time()
                )
                thread = threading.Thread(target=send_message, args=(article.author.email, msg))
                thread.start()  # 启动线程

    new_comment.save()

    return JsonResponse({"status": True})


@csrf_exempt
def comment_delete(request):
    if request.method == "GET":
        return JsonResponse({"status": False, "error": "评论失败，请求方式不正确。"})

    comment_id = request.POST.get("comment_id")
    sender_id = request.session.get("info").get("id")
    print(comment_id)
    print(sender_id)
    comment = Comment.objects.filter(id=comment_id, sender_id=sender_id, ).first()
    if not comment:
        return JsonResponse({"status": False, "error": "数据错误，评论失败。"})
    comment.delete()

    return JsonResponse({"status": True})
