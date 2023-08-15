from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank':True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    email_is_confirmed = models.BooleanField(default=False, verbose_name='подтверждено')
    email_confirm_key = models.CharField(max_length=30, verbose_name='ключ подтверждения почты', **NULLABLE)

    phone = models.CharField(max_length=25, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=120, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

