from django.template.loader import render_to_string
from django.core.signing import Signer

from my_house24.settings import ALLOWED_HOSTS
from .tasks import send_activation_letter

signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user,
               'host': host,
               'sign': signer.sign(user.email)}
    subject = render_to_string('users/elements/email/activation_letter_subject.txt', context)
    body_text = render_to_string('users/elements/email/activation_letter_body.txt', context)
    send_activation_letter(subject, body_text, user.email)
