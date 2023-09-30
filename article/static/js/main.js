//新增文章时候的预览效果
$('#yulan').click(
    function () {
        document.getElementById('yulanup').style.display = 'block'
        document.getElementById('yulandown').style.display = 'block'
    }
)

function hiddenyulan() {
    document.getElementById('yulanup').style.display = 'none'
    document.getElementById('yulandown').style.display = 'none'
}
$("#yulandown").click(
    function () {
        hiddenyulan()
    }
)


// 收藏文章
$("#shoucangbutton").click(
    function () {
        var nid = $(this).attr("article_id1")
        var nid2 = $(this).attr("article_id2")
        if (nid != nid2) {
            alert("错误！请不要修改网页源代码。")
            return
        }
        else {
            $.ajax({
                url: "/create/collect/",
                type: "get",
                dataType: 'JSON',
                data: { nid: nid },
                success: function (res) {
                    console.log(res)
                    if (res.status) {
                        alert("收藏成功！")
                    } else {
                        alert(res.error)
                    }
                }
            })
        }
    }
)
//关注博主
$("#getattention0").click(
    function () {
        var author_id = $(this).attr('author_id')
        $.ajax({
            url: "/user/add/attention/",
            type: "get",
            dataType: "JSON",
            data: {
                author_id: author_id
            },
            success: function (res) {
                if (res.status) {
                    alert('关注成功。')
                } else {
                    alert(res.error)
                }
                //location.reload()
            }
        })
    }
)






