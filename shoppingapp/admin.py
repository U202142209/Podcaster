from django.contrib import admin
from .models import QUser


# Register your models here.
@admin.register(QUser)
class CommentAdmin(admin.ModelAdmin):
    # readonly_fields = (
    #     'c_time', "xiaoyuanqiangpk", "nid", "img"
    # )
    #
    list_display = (
        'email', "username", 'ip', 'latest_edit', 'create_time'
    )
    # search_fields = ([
    #     "content", "userName", "nid", "fatherNid"
    # ])
