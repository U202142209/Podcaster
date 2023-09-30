from django.shortcuts import render, HttpResponse, redirect
from ..forms import ArticleAddModelForm, PageDivide
from django.http import JsonResponse
from ..config import get_nid, get_ip,get_now_time,send_message
from ..models import Article, Collect, Comment, Attention, Message
import threading

# 已发布的博客列表
def article_list(request):
    articls = Article.objects.filter(
        author_id=request.session['info']['id'],
        display=True,
        status=1,
    ).order_by("-create_time")

    return render(request, 'article_list.html', {
        "articles": articls,
    })


# 新增博客
def article_add(request):
    if request.method == "GET":
        form = ArticleAddModelForm()
        return render(request, 'article_add.html', {
            "form": form,
            # "message": "新增博客成功"
        })
    form = ArticleAddModelForm(data=request.POST)
    if form.is_valid():
        form.instance.nid = get_nid()
        form.instance.author_id = request.session['info']['id']
        form.instance.ip = get_ip(request)

        # 给粉丝发送更新通知
        if form.instance.status ==1 and form.instance.display and form.instance.publlic:
            attentions = Attention.objects.filter(host_id=request.session.get('info').get('id'))

            for attention in attentions:
                # 提醒所有的用户
                string = '<a target="_blank" href="/article/?nid=' + form.instance.nid + '"> ' + form.instance.title + ' </a>'
                bozhu = '<a target="_blank" href="/user/?id=' + str(
                    request.session.get('info').get('id')) + '"> ' + request.session.get('info').get(
                    'username') + ' </a>'
                msg=Message.objects.create(
                    sender_id=request.session.get('info').get('id'),
                    receiver_id=attention.guest_id,
                    content="  系统提醒； 你关注的博主 " + bozhu + " 发布了新的作品 " + string + ". 快去看看吧！。 "
                )

                # 是否具有发送邮箱的权限
                if attention.guest.new_article_remain:
                    # 首先判断是否具有发送邮箱的权限
                    ms ="  你关注的博主 %s(%s) 发布了新的博客 %s(%s) 、发布时间；%s 点击链接去查看详情吧！"%(
                        request.session.get('info').get('username'),
                        "http://101.43.229.177/user/?id="+ str(request.session.get('info').get('id')),
                        form.instance.title,
                        "http://101.43.229.177/article/?nid="+str( form.instance.nid ),
                        get_now_time()
                    )
                    try:
                        thread = threading.Thread(target=send_message, args=(msg.receiver.email, ms))
                        thread.start()  # 启动线程
                    except:
                        print("发送给 %s 的邮箱信息失败。"%msg.receiver.username)


        form.save()
        form = ArticleAddModelForm()
        return render(request, 'article_add.html', {
            "form": form,
            "message": "新增博客成功"
        })
    return render(request, 'article_add.html', {"form": form})


# 移动至回收站
def display_none(request):
    try:
        uid = request.GET.get("uid")
        obj = Article.objects.filter(nid=uid, author_id=request.session['info']['id'], display=True).first()
        print(obj)
        if not obj:
            return JsonResponse({"status": False, "error": "数据不存在"})
        obj.display = False
        obj.read_num = 0  # 阅读量
        # 取消收藏
        Collect.objects.filter(article_id=obj.id).delete()
        # 删除文章的评论
        Comment.objects.filter( article_id = obj.id ).delete()

        obj.save()
        return JsonResponse({"status": True})
    except:
        return JsonResponse({"status": False, "error": "数据不存在"})


# 博客具体详情页面
def article(request):
    nid = request.GET.get("nid")
    # 首先查找发布,且公开 的博客
    article = Article.objects.filter(
        nid=nid, status=1, publlic=True,
        display=True).first()
    if not article:
        # 如果没有找到公开的，就按照权限查找
        if not request.session.get('info'):
            return HttpResponse("没有找到相关博客，或者无权访问.<h2><a href='/'>点击返回首页</a> </h2>")
        article = Article.objects.filter(
            nid=nid, author_id=request.session.get('info').get('id'),
            display=True).first()
        if not article:
            return HttpResponse("博客不存在，或已被发布者删除，或者无权访问.<h2> <a href='/'>点击返回首页</a> </h2>")
    # 对公开的博客，阅读量加一
    if (not request.session.get(nid)) and (article.status == 1):
        request.session[nid] = nid  # 每个人只能阅读一次
        article.read_num += 1
        article.save()
    # 同一个作者的其他作品
    other_articles = Article.objects.filter(author_id=article.author_id,
                                            status=1, publlic=True, display=True,
                                            ).order_by("-create_time")
    # 获取评论的内容

    comments = Comment.objects.filter(article_id=article.id)
    return render(request, 'article.html', {
        "article": article,
        "other_articles": other_articles,
        "comments": comments,
    })


# 回收站页面
def recycle_list(request):
    articles = Article.objects.filter(author_id=request.session['info']['id'], display=False).order_by("-create_time")
    return render(request, 'recycle_list.html', {"articles": articles})


from django.views.decorators.csrf import csrf_exempt


# 彻底删除博客
@csrf_exempt
def article_recycle_to_draft(request):
    """定义；get请求恢复单个，post请求全部恢复"""
    if request.method == 'GET':
        nid = request.GET.get("uid")
        obj = Article.objects.filter(
            author_id=request.session['info']['id'],  # 验证是否为本人操作
            display=False,  # 是否在回收站
            nid=nid,  # 更具编号获取文章
        ).first()
        if obj:
            obj.status = 2
            obj.display = True
            obj.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": '恢复失败，数据不存在'})
    if request.method == 'POST':
        # 批量全部恢复
        objs = Article.objects.filter(author_id=request.session['info']['id'], display=False, )
        if objs:
            for obj in objs:
                obj.status = 2
                obj.display = True
                obj.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": '恢复失败，没有博客可以恢复至回收站。'})


# 草稿箱列表
def article_draft_list(request):
    articls = Article.objects.filter(
        author_id=request.session['info']['id'],
        display=True,
        status=2,
    ).order_by("-create_time")
    return render(request, 'article_draft_list.html', {"articles": articls})


@csrf_exempt
def article_delete_totally(request):
    if request.method == 'GET':
        nid = request.GET.get("uid")
        obj = Article.objects.filter(
            author_id=request.session['info']['id'],  # 验证是否为本人操作
            display=False,  # 是否在回收站
            nid=nid,  # 更具编号获取文章
        ).first()
        if obj:
            obj.delete()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False})

    obj = Article.objects.filter(
        author_id=request.session['info']['id'],  # 验证是否为本人操作
        display=False,  # 是否在回收站
    )
    if obj:
        obj.delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


# 编辑博客
def article_change(request, nid):
    article = Article.objects.filter(
        nid=nid, author_id=request.session['info']['id']
    ).first()
    if not article:
        return render(request, '404.html')
    form = ArticleAddModelForm(instance=article)

    if request.method == "GET":
        return render(request, 'article_add.html', {
            "form": form,
            "change": True,
        })
    form = ArticleAddModelForm(data=request.POST, instance=article)
    if form.is_valid():
        # form.instance.nid = get_nid()  # 刷新编号
        form.instance.ip = get_ip(request)  # 刷新IP

        # 给粉丝发送更新通知
        if form.instance.status==1 and form.instance.display and form.instance.publlic:
            attentions = Attention.objects.filter(host_id=request.session.get('info').get('id'))
            print(attentions)
            for attention in attentions:
                string = '<a target="_blank" href="/article/?nid=' + form.instance.nid + '"> ' + form.instance.title + ' </a>'
                bozhu = '<a target="_blank" href="/user/?id=' + str(
                    request.session.get('info').get('id')) + '"> ' + request.session.get('info').get(
                    'username') + ' </a>'
                msg=Message.objects.create(
                    sender_id=request.session.get('info').get('id'),
                    receiver_id=attention.guest_id,
                    content="  系统提醒； 你关注的博主 " + bozhu + " 发布了新的作品 " + string + ". 快去看看吧！。 "
                )

                # 是否具有发送邮箱的权限
                if attention.guest.new_article_remain:
                    # 首先判断是否具有发送邮箱的权限
                    ms = "  你关注的博主 %s(%s) 发布了新的博客 %s(%s) 、发布时间；%s 点击链接去查看详情吧！" % (
                        request.session.get('info').get('username'),
                        "http://101.43.229.177/user/?id=" + str(request.session.get('info').get('id')),
                        form.instance.title,
                        "http://101.43.229.177/article/?nid=" + str(form.instance.nid),
                        get_now_time()
                    )
                    try:
                        thread = threading.Thread(target=send_message, args=(msg.receiver.email, ms))
                        thread.start()  # 启动线程
                    except:
                        print("发送给 %s 的邮箱信息失败。" % msg.receiver.username)


        form.save()
        form = ArticleAddModelForm()
        print('编辑博客成功。')

        return render(request, 'article_add.html', {
            "form": form,
            "message": "编辑博客成功"
        })
    return render(request, 'article_add.html', {"form": form, "change": True, })
