from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ( "username","password","email","touxiang","ip" ,"create_time","latest_edit" )
    list_filter = ( "username","email" )
    search_fields = ( [ "username","email" ] )
    # readonly_fields = ('email',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ( "title","author","create_time","publlic","status","display","ip" )
    list_filter = ( "title","author","create_time","publlic","status","display" )
    search_fields = ( [ "title","author__username","create_time","publlic","status","display" ] )

class MessageAdmin(admin.ModelAdmin):
    list_display = ( "content" , 'receiver' ,"sender","read"  ,"create_time" )
    # list_filter = ( "title","author","create_time","publlic","status","display" )
    # search_fields = ( [ "title","author","create_time","publlic","status","display" ] )

class CommentAdmin(admin.ModelAdmin):
    list_display = ( "content" , 'parent',"reply_to" ,"sender" ,"article" , "create_time" )

class LinkAdmin(admin.ModelAdmin):
    list_display = ( "title","kind"  ,"create_time" )
    list_filter = ( "title","kind" )
    search_fields = ( [ "title","kind" ] )

class PhotoAdmin(admin.ModelAdmin):
    list_display = ( "title","img"  ,"create_time" )


admin.site.register(User,UserAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Message,MessageAdmin)
# admin.site.register(FirstComment)
# admin.site.register(SecondComment)
admin.site.register(Collect)
admin.site.register(Comment , CommentAdmin)

admin.site.register(Genre)
admin.site.register(Link,LinkAdmin)
# 资源下载
admin.site.register(Resource)

admin.site.register(Photos,PhotoAdmin)