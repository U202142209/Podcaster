import smtplib
from email.mime.text import MIMEText


def code():
    s = ''  # 创建字符串变量,存储生成的验证码
    # 只是用数字和大写字母
    for i in range(4):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        upper_alpha = chr(random.randint(65, 90))
        # lower_alpha = chr(random.randint(97, 122))
        # 从列表中 [], 返回一个随机元素
        # num = random.choice([num, upper_alpha, lower_alpha])
        num = random.choice([num, upper_alpha])
        s = s + str(num)
    return s


mail_host = 'smtp.qq.com'
port = 465

# send_by = '2869210303@qq.com'      # qq邮箱
# password = 'adnahbkerxzadege'      # 授权码

send_by='541689202@qq.com'      # 姐姐的小号邮箱
password='hcwufoalqlyebfeg'     # 姐姐的小号邮箱密码

def send_email(send_to,content ,subject="验证码"):
	#创建了MIMEText类，相当于在写邮件内容，是plain类型
    message = MIMEText(content,'plain','utf-8')
    message["From"] = send_by
    message['To'] = send_to
    message['Subject'] = subject
    #注意第三个参数，设置了转码的格式(我不设的时候会报解码错误)
    smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
    smpt.login(send_by,password)
    smpt.sendmail(send_by, send_to,message.as_string())
    print("发送成功")
    print(content)

def send_message(email , message ):
    try:
        message="【好记性博客共享平台】消息提醒 ； "+message
        send_email(email ,message ,subject="消息提醒")
        # 发送成功
        return True
    except:
        # 返回发送失败
        return False

def main(send_to):
    verificate_code=code()
    content=str('【好记性博客共享平台】你的验证码是；')+verificate_code+'  。如非本人操作，请忽略这条信息。'
    try:
        send_email(send_to,content)
        return verificate_code
    except:
        return False

def apiSebdEmailCode(send_to):
    verificate_code=code()
    content=str('【验证码】你的验证码是；')+verificate_code+'  。如非本人操作，请忽略这条信息。'
    try:
        send_email(send_to,content)
        return verificate_code
    except:
        return False

# X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def get_ip(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip

from datetime import datetime
import random
def get_nid():
    """产生随机数字"""
    return  datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))


import datetime as dt
def get_now_time():
    return dt.datetime.now().strftime('%F %T')


if __name__ == '__main__':
    sebt_to='2869210303@qq.com'
    # try:
    #     now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    #     send_email(sebt_to,'【消息提醒】。您在好记性博客网站 http://101.43.229.177  登录成功。登录时间；%s'%now_time)
    # except:
    #     print('error')
    code=main(sebt_to)
    print(code)

