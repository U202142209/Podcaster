//取消关注
function fun_attention_delete() {
    $('.attention_delete').click(
        function () {
            var r = confirm("你确定要取消关注吗？")
            if (r == true) {
                var host_id = $(this).attr('host_id')
                $.ajax({
                    url: '/attention/delete/',
                    type: "get",
                    data: { host_id: host_id },
                    dataType: 'JSON',
                    success: function (res) {
                        if (res.status) {
                            alert('取消关注成功。')
                            var thisele = document.getElementById('host_id_' + host_id)
                            // thisele.style.display='none'
                            thisele.parentNode.nextElementSibling.innerHTML = '<button class="attention_add btn-primary fontweight shubiao" host_id="' + host_id + '" id="add_id_' + host_id + '" type="button" onclick="attention_add()">关注</button>'

                            thisele.parentNode.removeChild(thisele)
                            //document.getElementById('add_id_' + host_id).style.display='block'
                            // <button class="attention_add btn-primary fontweight shubiao" host_id="{{attentio.host_id}}" id="add_id_{{attentio.host_id}}" type="button">关注</button>

                            //初始化
                            attention_add_init()
                        } else {
                            alert(res.error)
                        }
                    }
                })
            }
        }
    )
}
//初始化
fun_attention_delete()

//关注
function attention_add_init() {
    $(".attention_add").click(
        function attention_add() {
            var host_id = this.getAttribute("host_id")
            console.log(host_id)
            $.ajax({
                url: "/user/add/attention/",
                type: "get",
                dataType: "JSON",
                data: {
                    author_id: host_id
                },
                success: function (res) {
                    if (res.status) {
                        alert('关注成功。')
                        var attention_add_button = document.getElementById('add_id_' + host_id)
                        var div = attention_add_button.parentNode.previousElementSibling
                        console.log(div)
                        //  <button class="attention_delete btn-primary backred fontweight shubiao" host_id="{{attentio.host_id}}" id="host_id_{{attentio.host_id}}" type="button">取消关注</button>
                        div.innerHTML = ' <button class="attention_delete btn-primary backred fontweight shubiao" host_id="' + host_id + '" id="host_id_' + host_id + '" type="button">取消关注</button>'

                        attention_add_button.parentNode.removeChild(attention_add_button)
                        //出现取消关注按钮
                        fun_attention_delete()

                    } else {
                        alert(res.error)
                    }
                }
            })
        }
    )
}



