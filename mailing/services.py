from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Client
from django.utils import timezone


def send_message_email(mailing: object, email: list) -> None:
    send_mail(mailing.message.title,
              mailing.message.text,
              settings.EMAIL_HOST_USER,
              email
              )


def test():
    now_time = timezone.now().time()
    clients_email = list(
        Client.objects.values_list('email', flat=True)
    )

    print(now_time)
    mailing_list = Mailing.objects.filter(time=now_time)
    for mailing in mailing_list:
        if mailing.get_status() == 'started':
            send_message_email(mailing, clients_email)



