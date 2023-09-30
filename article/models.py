from ckeditor.fields import RichTextField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# 用户
class User(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=18)
    password = models.CharField(verbose_name="密码", max_length=40)
    email = models.EmailField(verbose_name="邮箱", max_length=40)

    touxiang = models.ImageField(
        verbose_name="头像",
        max_length=64,
        upload_to="touxiang/%Y/%m",
        null=True, blank=True,
        default="touxiang/user.png"
    )

    ip = models.CharField(verbose_name="ip属地", max_length=30, null=True, blank=True)

    create_time = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    latest_edit = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.username

    def article_num(self):
        return Article.objects.filter(author_id=self.id, status=1, display=True, ).count()

    def fensi(self):
        """粉丝数"""
        return Attention.objects.filter(host_id=self.id).count()

    def attention_num(self):
        """关注数"""
        return Attention.objects.filter(guest_id=self.id, ).count()

    def total_read_num(self):
        objs = Article.objects.filter(author_id=self.id, status=1, display=True, )
        sum = 0
        if objs:
            for obj in objs:
                sum = sum + obj.read_num
        return sum

    def total_collect_num(self):
        objs = Article.objects.filter(author_id=self.id, status=1, display=True, )
        sum = 0
        if objs:
            for obj in objs:
                sum = sum + obj.love_num()
        return sum

    # 判断这个人是否被关注
    def isAttentioned(self, fensi_id):
        if Attention.objects.filter(host_id=self.id, guest_id=fensi_id, ).first():
            return True
        return False

    """设置"""
    message_remain = models.BooleanField(verbose_name="我的博客收到评论,或有人回复我的评论时开通邮箱提醒", default=True)
    love_remain = models.BooleanField(verbose_name="我的博客被收藏时开通邮箱提醒", default=True)
    attention_remain = models.BooleanField(verbose_name="我被关注时开通邮箱提醒", default=True)
    new_article_remain = models.BooleanField(verbose_name="我关注的博主发布新作品时开通邮箱提醒", default=True)


# 博客模型
class Article(models.Model):
    author = models.ForeignKey(verbose_name="作者", to="User", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题", max_length=24)
    content = RichTextField(verbose_name="内容")

    # 这个保存的是最近编辑的时间
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    status_choices = (
        (1, "立即发表"), (2, "暂时存进草稿箱"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)
    publlic = models.BooleanField(verbose_name="是否公开")

    read_num = models.IntegerField(verbose_name="阅读量", default=0)
    ip = models.CharField(verbose_name="ip属地", max_length=30, null=True, blank=True)

    # display如果为false,则表示存进回收站
    display = models.BooleanField(verbose_name="是否可见", default=True)
    nid = models.CharField(max_length=20, verbose_name="编号")

    def __str__(self):
        return self.title

    def love_num(self):
        sun = Collect.objects.filter(article_id=self.id).count()
        if sum:
            return sun
        return 0




class Collect(models.Model):
    """收藏"""
    user = models.ForeignKey(verbose_name="用户", to="User", on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name="博客", to="Article", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    def __str__(self):
        str=self.user.username +"_______" +self.article.title
        return str

class Attention(models.Model):
    """关注"""
    host = models.ForeignKey(verbose_name="博主", to="User", on_delete=models.CASCADE,
                             related_name="arrention_host")
    guest = models.ForeignKey(verbose_name="粉丝", to="User", on_delete=models.CASCADE,
                              related_name="attention_guest")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


# 替换 models.Model 为 MPTTModel

class Comment(MPTTModel):
    # 新增，mptt树形结构
    content = RichTextField(verbose_name="评论内容")

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User, verbose_name="评论接收者",
        null=True, blank=True,
        on_delete=models.CASCADE, related_name='replyers'
    )

    sender = models.ForeignKey(
        User, verbose_name="评论发布者",
        on_delete=models.CASCADE, related_name='senders'
    )

    article = models.ForeignKey(
        Article, verbose_name="评论的文章",
        on_delete=models.CASCADE, related_name='article'
    )
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['-create_time']


class Genre(MPTTModel):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


# 消息类
class Message(models.Model):
    """
    消息一般是不可修改的，只读
    """
    content = models.CharField(verbose_name="内容", max_length=256)
    receiver = models.ForeignKey(verbose_name="收信人", to='User',
                                 on_delete=models.CASCADE, related_name="message_receiver")
    read = models.BooleanField(verbose_name="是否已读", default=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    sender = models.ForeignKey(verbose_name="发信人", to='User',
                               on_delete=models.CASCADE, related_name="message_sender")
    # 多级评论
    comment = models.ForeignKey(
        verbose_name="回复的评论",
        to="Comment",
        on_delete=models.CASCADE,
        null=True, blank=True)

    def __str__(self):
        return self.content

class Link(models.Model):
    title=models.CharField(max_length=60,verbose_name="标题")
    link=models.CharField(max_length=255,verbose_name="链接")
    kind_choices=(
        (1,"精彩推荐"),
        (2,"热门看点"),
        (3,"知识分享"),
    )

    kind=models.SmallIntegerField(verbose_name="分类",choices=kind_choices)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

import os
class Resource(models.Model):
    title=models.CharField(verbose_name="资源名称" , max_length=50)
    src=models.FileField(
        verbose_name="文件",
        max_length=128,
        upload_to="resources/%Y/%m",
    )

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.src.name)


class Photos(models.Model):
    img = models.ImageField(
        verbose_name="图片",
        max_length=64,
        upload_to="photos/%Y/%m/%d",
    )

    title=models.CharField(verbose_name="名称",max_length=32)

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title
