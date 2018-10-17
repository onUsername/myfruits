from celery import Celery
from django.core.mail import send_mail
import django
import os

# celery -A utils.tesk worker -l info
app =Celery("utils.tesk",broker="redis://192.168.12.216:6379/3")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myfruits.settings")
django.setup()


@app.task
def task_send_mail(subject,message,sender,receiver,html_message):
    import time
    print("发送邮件begin..")
    send_mail(subject,message,sender,receiver,html_message=html_message)
    print("发邮件end...")