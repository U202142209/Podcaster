var class_options = document.getElementById('class_options').querySelectorAll('span');
class_options[0].className = "ophover"
var displaykind = document.getElementById('displaykind').querySelectorAll("ul");
for (var i = 1; i < displaykind.length; i++) {
    displaykind[i].style.display = 'none'
}

for (var i = 0; i < class_options.length; i++) {
    console.log(111)
    class_options[i].onclick = function () {
        for (var i = 0; i < class_options.length; i++) {
            class_options[i].className = "none"
        }
        for (var i = 0; i < displaykind.length; i++) {
            displaykind[i].style.display = 'none'
        }
        data_index = this.getAttribute('data-index')
        displaykind[data_index].style.display = 'block'
        this.className = "ophover"
    }
}
//判断用户是否有权下载
$('.cannotdownload').click(
    function () {
        alert("您还没有登录，请先登录.")
    }
)