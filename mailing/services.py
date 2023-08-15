from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Mailing, Log
from django.utils import timezone


def send_message_email(mailing: object) -> None:
    send_result = send_mail(mailing.message.title,
              mailing.message.text,
              settings.EMAIL_HOST_USER,
              list(
                  mailing.clients.values_list('email', flat=True)
              )
              )
    now = timezone.now()
    if send_result:
        log_status = 'ok'
    else:
        log_status = 'failed'
    log = Log.objects.create(mailing=mailing, last_attempt=now, status=log_status)
    log.save()


def send_mailing():
    now = timezone.now()
    mailing_list = Mailing.objects.exclude(status='closed')
    print('lol')
    for mailing in mailing_list:
        last_send = mailing.log_set.filter(status='ok').order_by('last_attempt').first()
        send_message_email(mailing)
        print(last_send)

# def test():
#     now_time = timezone.now().time()
#     clients_email = list(
#         Client.objects.values_list('email', flat=True)
#     )
#
#     print(now_time)
#     mailing_list = Mailing.objects.filter(time=now_time)
#     for mailing in mailing_list:
#         if mailing.get_status() == 'started':
#             send_message_email(mailing, clients_email)



