from django.shortcuts import render, HttpResponse, redirect
from ..models import Message
from django.http import JsonResponse


# 默认未读消息
def message_list(request):
    messages = Message.objects.filter(
        receiver_id=request.session['info']['id'],
        read=False
    ).order_by('-create_time')
    messages_num = len(messages)
    read_messages_num = Message.objects.filter(
        receiver_id=request.session['info']['id'],
        read=True,
    ).count()
    return render(request, 'message_list.html', {
        "messages": messages,
        "messages_num": messages_num,
        "read_messages_num": read_messages_num,
        "sum": messages_num + read_messages_num,
        "type": "未读",
        "operator": "已读",
        "class": "fr message_to_read",
    })


# 获取已读消息
def message_read(request):
    messages = Message.objects.filter(
        receiver_id=request.session['info']['id'],
        read=True,
    ).order_by('-create_time')

    read_messages_num = len(messages)
    messages_num = Message.objects.filter(
        receiver_id=request.session['info']['id'],
        read=False,
    ).count()
    return render(request, 'message_list.html', {
        "messages": messages,
        "messages_num": messages_num,
        "read_messages_num": read_messages_num,
        "sum": messages_num + read_messages_num,
        "type": "已读",
        "operator": "未读",
        "class": "fr message_to_not_read",
    })


def message_delete(request):
    receiver_id = request.session.get('info').get('id')
    if request.GET.get("delete_read_all"):
        message = Message.objects.filter(receiver_id=receiver_id, read=True, )
        if message:
            message.delete()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": "数据不存在！"})
    if request.GET.get("delete_not_read_all"):
        message = Message.objects.filter(receiver_id=receiver_id, read=False, )
        if message:
            message.delete()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": "数据不存在！"})

    id = request.GET.get('nid')
    message = Message.objects.filter(
        receiver_id=receiver_id,
        id=id,
    ).first()
    if message:
        message.delete()
        return JsonResponse({"status": True, "id": id})
    return JsonResponse({"status": False, "error": "数据不存在！", "id": id})


# 标为已读消息
def message_to_read(request):
    receiver_id = request.session.get('info').get('id')
    if request.GET.get('all'):
        message = Message.objects.filter(
            receiver_id=receiver_id, read=False,
        )
        if message:
            message.update(read=True)  # 更高效的更新数据的方式
            # for msg in message:
            #     msg.read = True
            #     msg.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": "数据不存在！"})

    id = request.GET.get('nid')
    message = Message.objects.filter(
        receiver_id=receiver_id, id=id, read=False,
    ).first()
    if message:
        message.read = True
        message.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "数据不存在！"})


# 标为未读消息
def message_to_not_read(request):
    receiver_id = request.session.get('info').get('id')
    if request.GET.get('all'):
        message = Message.objects.filter(
            receiver_id=receiver_id, read=True,
        )
        if message:
            message.update(read=False)  # 更高效的更新数据的方式
            # for msg in message:
            #     msg.read = False
            #     msg.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, "error": "数据不存在！"})

    id = request.GET.get('nid')
    message = Message.objects.filter(
        receiver_id=receiver_id, id=id, read=True,
    ).first()
    if message:
        message.read = False
        message.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "数据不存在！", "id": id})
