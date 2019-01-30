from celery import Celery
from django.core.mail import send_mail
from django.conf import settings


# 使用celery

# 在工作者一端，由于未启动django项目，因此需要进行django初始化
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firekiss.settings")
django.setup()

# 启用工作者worker
# 需要拷贝一份项目代码到worker所在的机器上
# 启动指令(所在文件，信息等级)
# celery -A celery_task.tasks worker -l info


# 创建一个Celery对象,并指明中间人(broker)
app = Celery('celery_task.tasks', broker='redis://192.168.0.100:6379/0')


# 定义任务函数，并用celery对象的task方法进行装饰
@app.task
def send_confirm_mail(to_mail, username, token):
    """发送注册激活邮件"""

    subject = '欢迎来到FIREKISS 火吻'  # 主题
    message = ''  # 正文
    sender = settings.EMAIL_HOST_USER  # 发件人
    recceiver = [to_mail]  # 收件人
    # 正文包含html内容
    html_message = '<h1>%s,欢迎来到火吻商城</h1><p>请点击下面的链接完成账户激活,链接在24小时候后失效</p><p><a href="http://192.168.0.100:8000/user/active/%s">http://192.168.0.100:8000/user/active/%s</a></p>' % (
    username, token, token)

    send_mail(subject, message, sender, recceiver, html_message=html_message)
