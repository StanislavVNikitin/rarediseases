from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _

class MailFeedbackForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label=_("Тема"),)
    message = forms.CharField(widget=forms.Textarea, help_text=_("Напишите ваше сообщение"),label=_("Сообщение"),)
    captcha = CaptchaField()