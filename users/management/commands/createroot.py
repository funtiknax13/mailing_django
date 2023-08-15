from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = input('Введите email: ')
        first_name = input('Введите имя: ')
        last_name = input('Введите фамилию: ')

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        while True:
            password = input('Введите пароль: ')
            password2 = input('Повторите пароль: ')
            if password == password2:
                user.set_password(password)
                user.save()
                break
            else:
                print('Введенные пароли не совпадают, повторите попытку.')