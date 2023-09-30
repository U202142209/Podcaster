import random
import smtplib
from email.mime.text import MIMEText
import traceback

class EmailService:
    mail_host = 'smtp.qq.com'
    # mail_host = 'smtp.exmail.qq.com'
    port = 465
    send_by = '541689202@qq.com'  # 姐姐的小号邮箱
    password = 'hcwufoalqlyebfeg'  # 姐姐的小号邮箱密码
    @staticmethod
    def code():
        s = ""
        for i in range(4):
            num = random.randint(0, 9)
            upper_alpha = chr(random.randint(65, 90))
            num = random.choice([num, upper_alpha])
            s = s + str(num)
        return s

    @staticmethod
    def send_email(send_to, content, subject="验证码"):
        message = MIMEText(content, 'plain', 'utf-8')
        message["From"] = EmailService.send_by
        message['To'] = send_to
        message['Subject'] = subject
        smpt = smtplib.SMTP_SSL(EmailService.mail_host, EmailService.port, 'utf-8')
        smpt.login(EmailService.send_by, EmailService.password)
        smpt.sendmail(EmailService.send_by, send_to, message.as_string())

    @staticmethod
    def send_message(email, message, subject="消息提醒"):
        try:
            message = "【贝壳大家庭】消息提醒 ； " + message
            EmailService.send_email(email, message, subject=subject)
            return True
        except:
            # 返回发送失败
            return False

    @staticmethod
    def sendVerificateCode(send_to):
        verificate_code = EmailService.code()
        content = str('【贝壳校园墙网页版】您的验证码是；') + verificate_code + '  。如非本人操作，请忽略这条信息。'
        try:
            EmailService.send_email(send_to, content)
            return verificate_code
        except Exception as error:
            traceback.print_exc()
            return False


if __name__ == '__main__':
    sebt_to = '2869210303@qq.com'
    service = EmailService()
    code = service.sendVerificateCode(send_to=sebt_to)
    print(code)
    # res = EmailService.send_message(email=sebt_to, message="用户小明回复了你的评论，回复内容：是开发凯撒附件")
    # print(res)

