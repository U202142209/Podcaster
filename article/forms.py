from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import *


class RegisterModelForm(forms.ModelForm):
    # 新增确认密码
    conform_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    code = forms.CharField(label="邮箱验证码")

    class Meta:
        model = User
        fields = ["username", "email", "code", "password", "conform_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "input2",
                "placeholder": field.label
            }


class EmailLoginForm(forms.Form):
    email = forms.CharField(
        label="请输入邮箱"
    )

    code = forms.CharField(
        label="邮箱验证码",
        widget=forms.TextInput(
            attrs={
                "class": "input2",
                "placeholder": "验证码"
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "input2",
                "placeholder": field.label
            }


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(
            attrs={
                "class": "input2",
                "placeholder": "用户名/邮箱"
            }
        )
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={
                "class": "input2",
                "placeholder": "密码"
            }
        )
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={
                "class": "input2",
                "placeholder": "验证码"
            }
        )
    )


class ArticleAddModelForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'ckeditor',
    #             'name': 'content',
    #             "rows": "20",
    #             "cols": "50"
    #         }), label='博客内容', required=True, )

    content = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={
                'class': 'ckeditor',
                'name': 'content',
                # "rows": "20",
                # "cols": "50"
            }), label='内容', required=True, )

    class Meta:
        model = Article
        fields = ["title", "content", "status", "publlic"]

    # 展示样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "input3",
                "placeholder": field.label
            }


class PageDivide:
    """
    <a href="?page=1"><li>1</li></a>
    <a href="?page=2"><li>1</li></a>
    <a href="?page=3"><li>1</li></a>
    <a href="?page=4"><li>1</li></a>
    """
    """
    本类的作用是对Django的数据进行分页
    参数说明
    传入值
    request    # 请求对象
    queryset   # 需要操作的数据库
    div_column # 查询的字段
    pagesize   # 每一页的查询数量，默认=10
    plus       # 前后展示多少也，默认  = 5
    filter_column  # 排序，默认id，如果需要降序排序，输入-id


    返回值
    self.objects=prettys         # 返回的数据列表
    self.value=value             # 请求的参数q
    self.num=total_count         # 查询到指定条件的数据条数
    self.pagestring=page_string  # 返回分页的html代码，当前页的class="backblue"



    # 在.html文件中粘贴如下代码，
    <div class="div_page">
        {{page_string | safe }}
    </div>



    # 分页的css样式
    /* 分页 */
    .div_page li {
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        width: 40px;
        height: 40px;
        float: left;
        margin: 10px 1px;
        border: 1px solid blue;
    }

    .div_page li:hover ,.backblue {
        background-color: rgb(106, 189, 234);
        color: white;
    }
    """

    def __init__(self, request, queryset, div_column, pagesize=10, plus=5, filter_column="id"):
        data = {}  # 空字典查询所有
        value = request.GET.get("q")  # 如果游参数
        if value:
            data = {div_column + "__contains": value}
        else:
            value = ""
        # 判断页面是否有效
        if request.GET.get("page"):
            page = int(request.GET.get("page"))
        else:
            page = 1
        start = pagesize * (page - 1)
        end = pagesize * page

        total_count = queryset.objects.filter(**data).count()
        total_page_count, div = divmod(total_count, pagesize)
        if div:
            total_page_count += 1
        if total_page_count <= 2 * plus + 1:
            start_page = 1
            end_page = total_page_count
        else:
            if page <= plus:
                start_page = 1
                end_page = 2 * plus + 1
            else:
                if (page + plus) > total_page_count:
                    start_page = page - 2 * plus
                    end_page = total_page_count
                else:
                    # 数据库中有很多数据，需要分页
                    start_page = page - plus
                    end_page = page + plus

        page_str_list = []  # 返回的 html 代码
        # 首页
        tpl_ele = '<a href="?page=1&q=' + value + '"><li>首页</li></a>'
        page_str_list.append(tpl_ele)
        for i in range(start_page, end_page + 1):
            if i == page:
                tpl_ele = '<a href="?page={}&q={}"><li class="backblue" >{}</li></a>'.format(i, value, i)
            else:
                tpl_ele = '<a href="?page={}&q={}"><li>{}</li></a>'.format(i, value, i)
            page_str_list.append(tpl_ele)
        # 尾页
        tpl_ele = '<a href="?page=' + str(total_page_count) + '&q=' + value + '"><li>尾页</li></a>'
        page_str_list.append(tpl_ele)
        page_string = "".join(page_str_list)

        prettys = queryset.objects.filter(**data).order_by(filter_column)[start:end]

        self.objects = prettys
        self.value = value
        self.num = total_count
        self.pagestring = page_string


class SettingsModelForm(forms.ModelForm):
    """用户设置"""

    class Meta:
        model = User
        fields = ["username",
                  "message_remain",
                  "love_remain",
                  "attention_remain",
                  "new_article_remain",
                  ]

    # 展示样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'username':
                field.widget.attrs = {
                    "class": "switch switch-info",
                    # "placeholder": field.label
                }
            else:
                field.widget.attrs = {
                    "class": "input3",
                    "placeholder": field.label
                }


from django.core.exceptions import ValidationError


class SecurityModelForm(forms.ModelForm):
    """用户设置"""
    # 新增确认密码
    password = forms.CharField(
        label="请输入新密码",
        widget=forms.PasswordInput(
            render_value=True,  # 密码保存
        ), )

    conform_password = forms.CharField(label="确认新密码", widget=forms.PasswordInput(
        render_value=True,
    ))
    code = forms.CharField(label="邮箱验证码")

    class Meta:
        model = User
        fields = [
            "code", "password", "conform_password",
        ]

    # 展示样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "input3",
                "placeholder": field.label
            }

    # 判断两次的密码是否一致
    def clean_conform_password(self):
        txt_conform_password = self.cleaned_data['conform_password']
        if txt_conform_password != self.cleaned_data['password']:
            raise ValidationError('两次输入的密码不一致，请重新输入。')
        return txt_conform_password


class TouxiangChangeModelForm(forms.ModelForm):
    touxiang = forms.ImageField(label='上传头像')

    class Meta:
        model = User
        fields = ["touxiang"]

    # 展示样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "input3",
                "placeholder": field.label,
                " accept": "image/*",
                # "placeholder": field.label
            }
