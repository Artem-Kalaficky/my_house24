from django.core.mail import send_mail

from my_house24.celery import *


@app.task
def send_activation_letter(subject, body_text, email):
    return send_mail(subject, body_text, None, [email], fail_silently=False)
