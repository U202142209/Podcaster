# get_title

from django import template

register = template.Library()  # 注意变量名必须为register,不可改变



# 2、自定义标签
@register.simple_tag
def my_multi_tag(v1, v2):  # 自定义的标签可以定义多个参数
    return v1 * v2


# 3、自定义标签扩展之mark_safe
# 注释：我们可以用内置的标签safe来让标签内容有语法意义，如果我们想让自定义标签处理的结果也有语法意义，则不能使用内置标签safe了，需要使用mark_safe，可以实现与内置标签safe同样的功能
from django.utils.safestring import mark_safe


@register.simple_tag
def my_input_tag(id, name):
    res = "<input type='text' id='%s' name='%s' />" % (id, name)
    return mark_safe(res)


""""
怎么使用
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<!--必须先加载存有自定义过滤器和标签的文件-->
{% load my_tags %}

<!--salary的值为10，经过滤器my_multi_filter的处理结果为120-->
{{ salary|my_multi_filter:12 }}

<!--结果为2-->
{% my_multi_tag 1 2 %}

<!--
结果为一个input标签，该表的属性id="inp1" name="username"
注意：input的属性值均为字符串类型，所以my_input_tag后的两个值均为字符串类型
-->
{% my_input_tag "inp1" "username" %} 

</body>
</html>

"""

@register.filter
def get_title(arg):
    if len(arg)>=16:
        return arg[0:15]+". . ."
    return arg

@register.filter
def get_time(arg):
    print(arg)
    arg=str(arg)
    arg=arg.split("年","月","日")
    arg=" ".join(arg)
    return arg
