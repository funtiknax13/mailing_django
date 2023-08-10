from django.db import models

from django.utils import timezone


NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    email = models.CharField(max_length=200, verbose_name='E-mail')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Тема')
    text = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Mailing(models.Model):
    PERIODICITY_CHOICE = (
        ("day", "день"),
        ("week", "неделя"),
        ("month", "месяц"),
    )

    STATUS_CHOICE = (
        ("created", "Создана"),
        ("closed", "Завершена"),
        ("started", "Запущена"),
    )

    start_time = models.DateTimeField(verbose_name='Старт рассылки')
    end_time = models.DateTimeField(verbose_name='Завершение рассылки')
    time = models.TimeField(verbose_name='Время рассылки')
    periodicity = models.CharField(max_length=5, choices=PERIODICITY_CHOICE, default='day', verbose_name='Периодичность')
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, default='created', verbose_name='Статус')
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)

    def get_status(self):
        now = timezone.now()
        if self.start_time < now < self.end_time:
            self.status = "started"
        elif now > self.end_time:
            self.status = "closed"
        return self.status

    def __str__(self):
        return f'{self.message}: {self.time} (once a {self.periodicity})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    STATUS_CHOICE = (
        ("success", "Исполнена"),
        ("failed", "Провалена"),
    )
    mailing = models.ForeignKey(Mailing, verbose_name='Рассылка', on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(verbose_name='Время последней попытки')
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, verbose_name='Статус попытки')
    mail_response = models.CharField(max_length=250, verbose_name='Ответ почтового сервиса')

    def __str__(self):
        return f'{self.mailing} ({self.last_attempt}) - {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'
