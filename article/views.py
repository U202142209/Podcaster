from django.http import HttpResponse
from django.shortcuts import render

from .forms import PageDivide
from .models import Article, Link, Resource


# Create your views here.
# 首页
def index(request):
    # ip=get_ip(request)
    # print(ip)
    articles = Article.objects.filter(
        status=1,
        display=True,
        publlic=True,
    ).order_by("-create_time")[0:20]

    recs = Link.objects.filter(kind=1, ).order_by("-create_time")[0:10]

    hots = Link.objects.filter(kind=2, ).order_by("-create_time")[0:10]

    konws = Link.objects.filter(kind=3, ).order_by("-create_time")[0:10]
    return render(request, 'index.html', {
        "articles": articles,
        "recs": recs,
        "knows": konws,
        "hots": hots,

    })


from io import BytesIO  # 内存中的文件
from .imgcode import gen_verified_image


def random_img(request):
    image, verify = gen_verified_image()
    stream = BytesIO()
    image.save(stream, 'png')

    request.session["image_code"] = verify
    # 验证码 60 秒内有效
    request.session.set_expiry(60)
    print(verify)
    return HttpResponse(stream.getvalue())


def get_more_hots(requests):
    type = requests.GET.get('type')

    # 默认展示热榜
    nodes = Link.objects.filter(kind=2, ).order_by("-create_time")
    title = "热门推送"
    if type == "recs":
        nodes = Link.objects.filter(kind=1, ).order_by("-create_time")
        title = "精彩推荐"
    if type == "knows":
        nodes = Link.objects.filter(kind=3, ).order_by("-create_time")
        title = "知识分享"
    if type == "articls":
        articles = articles = Article.objects.filter(
            status=1, display=True, publlic=True, ).order_by("-create_time")
        return render(requests, 'list.html', {
            "articles": articles,
        })

    return render(requests, 'list.html', {
        "nodes": nodes,
        "title": title,
    })


# 下载
def download(request):
    obj = PageDivide(
        request=request,  # 请求对象
        queryset=Resource,  # 数据表
        div_column="title",  # 查询字段
        pagesize=10,  # 每页的数据数量
        plus=5,  # 前后的页数
        filter_column="-create_time"  # 按照时间排序
    )

    return render(request, 'download.html', {
        "resources": obj.objects,
        "num": obj.num,
        "value": obj.value,
        "page_string": obj.pagestring
    })


# 全局搜索
def search(request):
    q = request.GET.get('q')
    articles = Article.objects.filter(
        publlic=True, status=1, display=True,
        title__contains=q,
    ).order_by("-create_time")
    links = Link.objects.filter(title__contains=q, ).order_by("-create_time")
    resources = Resource.objects.filter(title__contains=q, ).order_by("-create_time")
    return render(request, 'search.html', {
        "q": q,
        "articles": articles,
        "links": links,
        "resources": resources,

    })


def page_not_found(request):
    return render(request, '404.html')


# def server_error(request):
#     return render(request, '500.html')
#
#
# def bad_request(request):
#     return render(request, '400.html')


from .models import Genre


def test_mptt(request):
    return render(request, 'genre.html', {'genres': Genre.objects.all()})
