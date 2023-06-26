from typing import Dict, Union
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    send_mail(
        "site Rare diseases",  # subject (title)
        message_form["message"],  # message
        ["test@mail.ru"],  # send from
        ["test@mail.ru"],  # send to
        fail_silently=False,
    )
    return None
