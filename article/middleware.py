import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect

class MiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # print(request.path_info)


        if request.session.get("info"):
            return
        else:
            # request.path_info 用户访问的url
            accetp_urls = [
                "/admin/login/",  # 超级管理员
                "/login/",          # 登录
                "/",                # 首页
                "/register/",       # 注册
                "/random_img/",     # 图片验证码
                "/getemailcode/",   # 邮箱验证码
                "/article/",        # 博客详情页
                "/create/collect/",# 收藏作品
                "/user/add/attention/",   # 关注博主
                "/user/",                 # 用户详情页
                "/post-comment/",         # 评论
                '/download/',            # 资源下载
                '/search/',              # 搜索
                '/show/more/hots/',     # 加载更多
                '/login/email/',        # 邮箱免密码登录
                '/api/sendemailcode/',# 邮箱验证码

            ]

            if request.path_info in accetp_urls:
                return
            else:
                pattern = r'^static/.*'
                # print(pattern)
                # print(request.path_info)
                # 如果匹配失败，返回 NONE
                match = re.search(pattern, request.path)

                if not match:
                    return
                return redirect("/login/?message=你还没有登录，无权访问，请先登录")
            # return

    def process_response(self, request, response):
        return response
