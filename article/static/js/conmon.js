//搜索框的聚焦效果
var search1 = document.getElementById('search1')
search1.onfocus = function () {
    this.className = "search1 input1"
}

//弹出登录框
$("#login0").click(
    function () {
        document.getElementById('light').style.display = 'block';
        document.getElementById('fade').style.display = 'block'
    }
)

//切换图片验证码
$("#imgcontainer").click(
    function () {
        console.log(123)
        var img = document.getElementById("code1234")
        console.log(img)
        img.src = "/random_img/"
    }
)

//判断用户是否有权下载
$('.cannotdownload').click(
    function () {
        alert("您还没有登录，请先登录.")
    }
)







