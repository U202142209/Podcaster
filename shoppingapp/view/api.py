# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: api.py
 @time: 2023/8/14 8:07
  '''

"""
接口设计
1.查看全部 （新发、新回、最热、精选）
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=10&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=0&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=1&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=2&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D&type=3&campus=1
2.吐槽（新发、新回、最热、精选）
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%5D&type=0&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%5D&type=1&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%5D&type=2&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio4%22%2C%22radio40%22%5D&type=3&campus=1
3.表白（新发、新回、最热、精选）
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio41%22%5D&type=0&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio41%22%5D&type=1&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio41%22%5D&type=2&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio41%22%5D&type=3&campus=1
4.心愿（新发、新回、最热、精选）
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio42%22%5D&type=0&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio42%22%5D&type=1&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio42%22%5D&type=2&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio42%22%5D&type=3&campus=1
5.知乎（新发、新回、最热、精选）
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio43%22%5D&type=0&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio43%22%5D&type=1&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio43%22%5D&type=2&campus=1
https://www.yqtech.ltd:8802/gettaskbyTypeQuanzi?length=0&radioGroup=%5B%22radio43%22%5D&type=3&campus=1
10.用户发布的
https://www.yqtech.ltd:8802/gettaskbyOpenIdQuanzi?openid=o7FW15WQQQakCpA12B2HhQ4GykGE&length=0
11.用户喜欢的
https://www.yqtech.ltd:8802/getlikeByOpenidQuanzi?openid=o7FW15WQQQakCpA12B2HhQ4GykGE&length=0
12.用户评论的
https://www.yqtech.ltd:8802/getCommentByOpenidQuanzi?openid=o7FW15WQQQakCpA12B2HhQ4GykGE&length=0
https://www.yqtech.ltd:8802/getCommentByOpenidQuanzi?openid=o7FW15WQQQakCpA12B2HhQ4GykGE&length=10
https://www.yqtech.ltd:8802/getCommentByOpenidQuanzi?openid=o7FW15WQQQakCpA12B2HhQ4GykGE&length=20
13.用户回复通知
https://www.yqtech.ltd:8802/getCommentByApplytoQuanzi?applyTo=o7FW15WQQQakCpA12B2HhQ4GykGE&length=0
https://www.yqtech.ltd:8802/getCommentByApplytoQuanzi?applyTo=o7FW15WQQQakCpA12B2HhQ4GykGE&length=10
https://www.yqtech.ltd:8802/getCommentByApplytoQuanzi?applyTo=o7FW15WQQQakCpA12B2HhQ4GykGE&length=16
14.搜索帖子
https://www.yqtech.ltd:8802/gettaskbySearchQuanzi?search=%E8%AE%A1%E7%AE%97%E6%9C%BA&length=0&campus=1
https://www.yqtech.ltd:8802/gettaskbySearchQuanzi?search=%E8%AE%A1%E7%AE%97%E6%9C%BA&length=10&campus=1
15.帖子详情
https://www.yqtech.ltd:8802/gettaskbyIdQuanzi?pk=59642
16.帖子评论
https://www.yqtech.ltd:8802/getCommentByTypeQuanzi?length=6&pk=58581&type=0
17..删除评论
https://www.yqtech.ltd:8802/deleteCommentQuanzi?pk=
"""

import warnings

import requests

warnings.filterwarnings("ignore")
BASEURL = "https://www.yqtech.ltd:8802"


def getTieZi(
        currentPage=0,
        radioGroup="%5B%22radio4%22%2C%22radio40%22%2C%22radio41%22%2C%22radio42%22%2C%22radio43%22%5D",
        type="0",
):
    urls = [
        f"{BASEURL}/gettaskbyTypeQuanzi?length={str((2 * currentPage) * 10)}&radioGroup={radioGroup}&type={type}&campus=1",
        f"{BASEURL}/gettaskbyTypeQuanzi?length={str((2 * currentPage + 1) * 10)}&radioGroup={radioGroup}&type={type}&campus=1",
    ]
    try:
        taskList = []
        for url in urls:
            res = requests.get(url=url)
            datas = res.json()["taskList"]
            taskList.extend(datas)
        return taskList
    except Exception as e:
        return []


def search(keyword="", currentPage=0):
    urls = [
        f"{BASEURL}/gettaskbySearchQuanzi?search={keyword}&length={str((2 * currentPage) * 10)}&campus=1",
        f"{BASEURL}/gettaskbySearchQuanzi?search={keyword}&length={str((2 * currentPage + 1) * 10)}&campus=1",
    ]
    try:
        taskList = []
        for url in urls:
            res = requests.get(url=url)
            # print(res.url)
            datas = res.json()["taskList"]
            taskList.extend(datas)
        return taskList
    except Exception as e:
        return []


def getTieZiDetail(pk=10000):
    try:
        return requests.get(f"{BASEURL}/gettaskbyIdQuanzi?pk={str(pk)}").json()["taskList"][0]
    except:
        return []


def getTieZiByOpenid(openid="o7FW15Xeu8-ZRHmmDwfH0ezT9hII", length=0):
    try:
        return requests.get(
            url=f"{BASEURL}/gettaskbyOpenIdQuanzi",
            params={"openid": openid, "length": length * 10}, verify=False
        ).json()["taskList"]
    except:
        return []


def getLikedByOpenid(openid="o7FW15Xeu8-ZRHmmDwfH0ezT9hII", length=0):
    try:
        return requests.get(
            url=f"{BASEURL}/getlikeByOpenidQuanzi",
            params={"openid": openid, "length": length * 10}, verify=False
        ).json()["likeList"]
    except:
        return []


def getCommentsByOpenid(openid="o7FW15Xeu8-ZRHmmDwfH0ezT9hII", length=0):
    try:
        return requests.get(
            url=f"{BASEURL}/getCommentByOpenidQuanzi",
            params={"openid": openid, "length": length * 10}, verify=False
        ).json()["commentList"]
    except:
        return []


def getMessageByOpenid(openid="o7FW15Xeu8-ZRHmmDwfH0ezT9hII", length=0):
    try:
        return requests.get(
            url=f"{BASEURL}/getCommentByApplytoQuanzi",
            params={"applyTo": openid, "length": length * 10}, verify=False
        ).json()["commentList"]
    except:
        return []


def getCommentByTypeQuanzi(pk, length=0):
    try:
        return requests.get(
            url=f"{BASEURL}/getCommentByTypeQuanzi",
            params={"pk": pk, "length": length * 10, "type": 0}, verify=False
        ).json()["commentList"]
    except:
        return []


from django.http import JsonResponse


def setError(msg):
    return JsonResponse({
        "code": 500,
        "status": False,
        "msg": msg,
        "data": [],
    }, json_dumps_params={'ensure_ascii': False},
        content_type="application/json; charset=utf-8")


def setSuccess(msg, data=None):
    return JsonResponse({
        "code": 200,
        "status": True,
        "msg": msg,
        "data": data,
    },
        json_dumps_params={'ensure_ascii': False},
        content_type="application/json; charset=utf-8")


def deleteCommentByCommentPk(pk):
    return requests.get(
        url="https://www.yqtech.ltd:8802/deleteCommentQuanzi?pk=" + str(pk),
        verify=False,
    ).json()


def getAllCommentByTuanziId(tieziId):
    dic = getCommentByTypeQuanzi(tieziId)
    # 解析id
    commentIdList = []
    for comment in dic:
        commentIdList.append(comment["id"])
        for comment2 in comment["commentList"]:
            commentIdList.append(comment2["id"])
    print(dictToString(dic))
    print("commentIdList", commentIdList)
    return commentIdList


def deleteAllCommentByCommentIdList(commentIdList):
    for pk in commentIdList:
        print(deleteCommentByCommentPk(pk=pk))


def deleteAllCommentByTuanziId(tieziId):
    deleteAllCommentByCommentIdList(
        commentIdList=getAllCommentByTuanziId(
            tieziId=tieziId
        )
    )


def dictToString(dic):
    return str(dic).strip().replace("\'", "\"")


if __name__ == '__main__':
    print("测试")
    # print(str(getTieZi()).replace("\'", "\""))
    # keyword = "计算机"
    # # print(str(search(keyword=keyword)).replace("\'", "\""))
    # pk = 59675
    # print(str(getTieZiDetail(pk=pk)).replace("\'", "\""))
    pk = 61669
    # deleteAllCommentByTuanziId(pk)
    print(getAllCommentByTuanziId(pk))
