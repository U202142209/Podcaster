/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2006, 2014 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD (Register as an anonymous module)
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // Node/CommonJS
        module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {

    var pluses = /\+/g;

    function encode(s) {
        return config.raw ? s : encodeURIComponent(s);
    }

    function decode(s) {
        return config.raw ? s : decodeURIComponent(s);
    }

    function stringifyCookieValue(value) {
        return encode(config.json ? JSON.stringify(value) : String(value));
    }

    function parseCookieValue(s) {
        if (s.indexOf('"') === 0) {
            // This is a quoted cookie as according to RFC2068, unescape...
            s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
        }

        try {
            // Replace server-side written pluses with spaces.
            // If we can't decode the cookie, ignore it, it's unusable.
            // If we can't parse the cookie, ignore it, it's unusable.
            s = decodeURIComponent(s.replace(pluses, ' '));
            return config.json ? JSON.parse(s) : s;
        } catch (e) { }
    }

    function read(s, converter) {
        var value = config.raw ? s : parseCookieValue(s);
        return $.isFunction(converter) ? converter(value) : value;
    }

    var config = $.cookie = function (key, value, options) {

        // Write

        if (arguments.length > 1 && !$.isFunction(value)) {
            options = $.extend({}, config.defaults, options);

            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setMilliseconds(t.getMilliseconds() + days * 864e+5);
            }

            return (document.cookie = [
                encode(key), '=', stringifyCookieValue(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path ? '; path=' + options.path : '',
                options.domain ? '; domain=' + options.domain : '',
                options.secure ? '; secure' : ''
            ].join(''));
        }

        // Read

        var result = key ? undefined : {},
            // To prevent the for loop in the first place assign an empty array
            // in case there are no cookies at all. Also prevents odd result when
            // calling $.cookie().
            cookies = document.cookie ? document.cookie.split('; ') : [],
            i = 0,
            l = cookies.length;

        for (; i < l; i++) {
            var parts = cookies[i].split('='),
                name = decode(parts.shift()),
                cookie = parts.join('=');

            if (key === name) {
                // If second argument (value) is a function it's a converter...
                result = read(cookie, value);
                break;
            }

            // Prevent storing a cookie that we couldn't decode.
            if (!key && (cookie = read(cookie)) !== undefined) {
                result[name] = cookie;
            }
        }

        return result;
    };

    config.defaults = {};

    $.removeCookie = function (key, options) {
        // Must not alter options, thus extending a fresh object...
        $.cookie(key, '', $.extend({}, options, { expires: -1 }));
        return !$.cookie(key);
    };

}));
function getcommentdetails() {
    if (window.navigator.webdriver == true) {
        alert("Warnning ! 系统检测到爬虫，无法获取数据。")
    } else {
        $.ajax({
            type: "GET",
            url: "/shopping/detail/getdataapi",
            data: {
                pk: $("#xiaoyuanqiangdatacontent").attr("data-id"),
            },
            dataType: "JSON",
            success: function (res) {
                $("#xiaoyuanqiangdatacontent").html('')
                if (res.taskList != []) {
                    var data = res.taskList;
                    $.each(data, function (i, obj) {
                        var str = '';
                        str += '<div class="row"> <div class="col-xs-2"> <img width="100%" src="' + obj.avatar + '" alt=""><br><p class="tac">' + obj.id + '</p></div><div class="col-xs-9"> <p>用户:' + obj.userName + '</p><p>发帖时间:' + obj.c_time + '</p><p><span class="spanleft">阅读量:' + obj.watchNum + '</span><span class=".spanright">喜欢:' + obj.likeNum + '</span></p></div></div><div class="detail_article_content000"><p>' + obj.content + '</p></div>'
                        if (obj.img) {
                            str += ' <img width="100%" src="' + obj.img + '" alt="">'
                        }
                        $("#articlebody").append(str)
                        $("#comment_num_div").html("帖子评论 (" + obj.commentNum + ") ")
                    });
                    // get comment data next 
                    $.ajax({
                        type: "GET",
                        url: "/shopping/detail/getcommentapi/",
                        data: {
                            length: "0",
                            pk: $("#xiaoyuanqiangdatacontent").attr("data-id"),
                            type: "0",
                        },
                        dataType: "JSON",
                        success: function (cres) {
                            if (cres.commentList) {
                                $.each(cres.commentList, function (i, obj) {
                                    var str = '';
                                    str += '<div class="row comment_father"><div class="col-xs-2"> <img width="100%" src="' + obj.avatar + '" alt=""> </div><div class=" colxs-10"><div><p class="font_gray"> <span>' + obj.userName + '</span> </p><p>' + obj.comment + '</p><p class="font_gray"> <span><span>' + obj.c_time + '</span></span><span>点赞:' + obj.like_num + '</span></p></div></div><br>'
                                    if (obj.img) {
                                        str += ' <img width="90%" src="' + obj.img + '" alt="">'
                                    }
                                    if (obj.commentList) {
                                        $.each(obj.commentList, function (ci, commentobj) {
                                            str += '<div class="next_comments"><div><p><strong>---------------------------------------------</strong></p><p class="font_gray"><span class="spanleft">用户:' + commentobj.userName + '</span><span class="spanright">' + commentobj.c_time + '</span></p><p>评论内容: ' + commentobj.comment + '</p>'
                                            if (commentobj.img) {
                                                str += '<img src="' + commentobj.img + '" width="50%" alt="">'
                                            }
                                            str += '<br><br><p>喜欢:' + commentobj.ike_num + '</p></div></div></div>'
                                        })
                                    }
                                    $("#detail_comment_content").append(str)
                                })
                            }
                        },
                        error: function (args) {
                            alert("获取评论诗句失败，请刷新重试!")
                        }
                    })
                } else {
                    alert("获取数据失败，请刷新重试。")
                }
            },
            error: function (arg1) {
                alert("加载数据失败");
                // console.log(arg1);
            }
        });
    }
}


