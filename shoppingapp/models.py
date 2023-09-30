from django.db import models
from django.utils import timezone


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(
        verbose_name="创建时间",
        default=timezone.now,
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name="是否已经删除"
    )

    class Meta:
        abstract = True


class QUser(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=100, )
    email = models.EmailField(verbose_name="邮箱", max_length=100, unique=True)
    detail = models.TextField(verbose_name="个人简介", default="")
    ip = models.CharField(max_length=18, default="", verbose_name="用户IP地址")
    create_time = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    latest_edit = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    deleteTaskPower = models.BooleanField(default=False, verbose_name="删除帖子的权限")
    deleteCommentPower = models.BooleanField(default=False, verbose_name="删除帖子的权限")
    lookUseerDetailPower = models.BooleanField(default=False, verbose_name="查看其他用户详情页的权限")
    sendMessagePower = models.BooleanField(default=False, verbose_name="发送消息的权限")

    def __str__(self):
        return self.email
    class Meta:
        db_table = 'QUser'
