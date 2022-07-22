from django.core.mail import send_mail

from my_house24.celery import *


@app.task
def send_activation_letter(subject, body_text, email):
    return send_mail(subject, body_text, None, [email], fail_silently=False)


@app.task
def send_change_password_notification(email):
    return send_mail('Мой Дом 24', 'Ваш пароль успешно изменен. Никому не сообщайте новый пароль!', None, [email],
                     fail_silently=False)


@app.task
def send_invite_letter(email, body_text):
    return send_mail('Приглашение в Demo CRM 24', body_text, None, [email], fail_silently=False)



