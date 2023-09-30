import requests


def getAllData():
    i = 0
    while 1:
        url = f"https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length={str(i * 10)}&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=0&campus=1"
        try:
            res = requests.get(url=url)
            datas = res.json()["taskList"]
            for data in datas:
                id = data["id"]
                content = data["content"]
                price = data["price"]
                title = data["title"]
                avatar = data["avatar"]
                commentNum = data["commentNum"]
                c_time = data["c_time"]
                comment_time = data["comment_time"]
                print(id, c_time, content, price, title, avatar, commentNum, comment_time)
        except Exception as e:
            print("发生了错误；", e)
            break
        i = i + 1


def getAPageData(currentPage):
    """
    后端请求接口，获取二十条数据，currentPage取值 1 - 25
    result=[{
        "id":  ,
        "c_time": ,
        "content":,
        "title":,
        "avatar":,
        "commentNum":,
        "comment_time":,
    }]
    result=[ id, c_time, content, title, avatar, commentNum, comment_time ]
    """

    first = 2 * currentPage
    second = 2 * currentPage + 1

    result = {
        "code": 404,
        "data": [],
    }

    urls = [
        f"https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length={str(first * 10)}&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=0&campus=1",
        f"https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length={str(second * 10)}&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=0&campus=1",
        # https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=10&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=0&campus=1
    ]

    try:
        for url in urls:
            res = requests.get(url=url)
            datas = res.json()["taskList"]
            for data in datas:
                # price = data["price"]
                result["data"].append({
                    "id": data["id"],
                    "c_time": data["c_time"],
                    "content": data["content"],
                    "title": data["title"],
                    "avatar": data["avatar"],
                    "commentNum": data["commentNum"],
                    "comment_time": data["comment_time"],
                    "userName": data["userName"],
                    "openid": data["openid"],
                    "campusGroup": data["campusGroup"],
                    "watchNum": data["watchNum"],
                    "likeNum": data["likeNum"],
                    "radioGroup": data["radioGroup"],
                })
                # 修改code为成功
                result["code"] = 0
        # print(result)
        return result
    except Exception as e:
        print("发生了错误；", e)
        return result


from datetime import datetime
import random


def get_nid():
    """产生随机数字"""
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))


# 获取当前的页数
def getCurrentPage(currentPage):
    try:
        currentPage = int(currentPage)
        if currentPage < 0:
            currentPage = 0
    except:
        currentPage = 0
    finally:
        return currentPage


# 获取分页字符串
def getPageDividerString(currentPage):
    resultstring = ""
    for i in range(25):
        if i == currentPage:
            resultstring += f'<li class="active"><a href="/shopping/?currentPage={str(i)}">{str(i + 1)}</a></li>'
        else:
            resultstring += f'<li><a href="/shopping/?currentPage={str(i)}">{str(i + 1)}</a></li>'
    return resultstring



if __name__ == '__main__':
    # getAllData()
    print(getAPageData(
        currentPage=10
    ))
