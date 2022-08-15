import pdfkit
from django.core.mail import send_mail, EmailMessage
from xlsx2html import xlsx2html

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


@app.task
def send_invoice_in_pdf(email):
    xlsx2html('media/temp_files/invoice.xlsx', 'media/temp_files/invoice.html')
    pdfkit.from_file('media/temp_files/invoice.html', 'media/temp_files/invoice.pdf')
    email = EmailMessage('Demo CRM 24', 'Какой-то очень важный текст', None, [email])
    email.attach_file('media/temp_files/invoice.pdf')
    email.send()
    return 'Success PDF sending'






