from typing import Dict, Union
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    send_mail("Сообщение с сайта Редкиеболезни.рф", message_form["message"], settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL_ADDRESS], fail_silently=True
    return None
